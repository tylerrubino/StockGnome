# backend/api/views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import StockPredictionSerializer
from .utils import save_plot

from datetime import datetime
from functools import lru_cache
from pathlib import Path
import os
import pandas as pd
import yfinance as yf


@lru_cache(maxsize=1)
def ml_stack():
    """
    Lazily import heavy ML/plotting dependencies the first time they're needed,
    and cache the imports for all subsequent requests.
    """
    # Headless backend to avoid GUI/font-cache work that kills small instances
    os.environ.setdefault("MPLBACKEND", "Agg")

    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import mean_squared_error, r2_score
    from keras.models import load_model

    # Make sure pyplot uses Agg (in case mpl was imported elsewhere)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return {
        "np": np,
        "MinMaxScaler": MinMaxScaler,
        "mean_squared_error": mean_squared_error,
        "r2_score": r2_score,
        "load_model": load_model,
        "plt": plt,
    }


@lru_cache(maxsize=1)
def load_keras_model():
    """
    Load and cache the Keras model once. Looks in common locations or in the
    path provided by the STOCKGNOME_MODEL_PATH environment variable.
    """
    deps = ml_stack()
    load_model = deps["load_model"]

    candidates = [
        Path(settings.BASE_DIR) / "stock_prediction_model.keras",
        Path(__file__).resolve().parent / "stock_prediction_model.keras",
        Path(__file__).resolve().parent.parent / "stock_prediction_model.keras",
    ]

    env_path = os.environ.get("STOCKGNOME_MODEL_PATH")
    if env_path:
        candidates.insert(0, Path(env_path))

    for p in candidates:
        if p.exists():
            return load_model(str(p))

    raise FileNotFoundError(
        "stock_prediction_model.keras not found. "
        "Set STOCKGNOME_MODEL_PATH or place the model file in the project."
    )


class StockPredictionAPIView(APIView):
    """
    API View to handle stock predictions.
    """

    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ticker = serializer.validated_data["ticker"]

        # Fetch the stock data from yfinance (10 years)
        now = datetime.now()
        start = datetime(now.year - 10, now.month, now.day)
        end = now
        df = yf.download(ticker, start=start, end=end, progress=False)

        if df.empty:
            return Response(
                {"error": "No data found for the ticker"},
                status=status.HTTP_404_NOT_FOUND,
            )

        df = df.reset_index()

        # Import heavy deps lazily
        deps = ml_stack()
        np = deps["np"]
        MinMaxScaler = deps["MinMaxScaler"]
        mean_squared_error = deps["mean_squared_error"]
        r2_score = deps["r2_score"]
        plt = deps["plt"]

        # ---------- Basic Plot ----------
        plt.figure(figsize=(12, 5))
        plt.plot(df.Close, label="Closing Price")
        plt.title(f"Stock Closing Price for {ticker}")
        plt.xlabel("Days")
        plt.ylabel("Close Price")
        plt.legend()
        plot_img = save_plot(f"{ticker}_plot.png")

        # ---------- 100 DMA ----------
        ma100 = df.Close.rolling(window=100).mean()
        plt.figure(figsize=(12, 5))
        plt.plot(df.Close, label="Closing Price")
        plt.plot(ma100, "r", label="100 Days Moving Average")
        plt.title(f"100 DMA for {ticker}")
        plt.xlabel("Days")
        plt.ylabel("Close Price")
        plt.legend()
        plot_img_ma = save_plot(f"{ticker}_ma100_plot.png")

        # ---------- 200 DMA ----------
        ma200 = df.Close.rolling(window=200).mean()
        plt.figure(figsize=(12, 5))
        plt.plot(df.Close, label="Closing Price")
        plt.plot(ma100, "r", label="100 Days Moving Average")
        plt.plot(ma200, "g", label="200 Days Moving Average")
        plt.title(f"200 DMA for {ticker}")
        plt.xlabel("Days")
        plt.ylabel("Close Price")
        plt.legend()
        plot_img_ma200 = save_plot(f"{ticker}_ma200_plot.png")

        # ---------- Train/Test Split ----------
        data_training = pd.DataFrame(df.Close[0 : int(len(df) * 0.70)])
        data_testing = pd.DataFrame(df.Close[int(len(df) * 0.70) : int(len(df))])

        # ---------- Scaling ----------
        scaler = MinMaxScaler(feature_range=(0, 1))

        # ---------- Load Model (cached) ----------
        try:
            model = load_keras_model()
        except FileNotFoundError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # ---------- Prepare Test Data ----------
        past_100_days = data_training.tail(100)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = scaler.fit_transform(final_df)

        x_test, y_test = [], []
        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i - 100 : i])
            y_test.append(input_data[i, 0])

        x_test = np.array(x_test)
        y_test = np.array(y_test)

        # ---------- Predict ----------
        y_predicted = model.predict(x_test, verbose=0)

        # ---------- Inverse Scale ----------
        y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
        y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

        # ---------- Final Prediction Plot ----------
        plt.figure(figsize=(12, 5))
        plt.plot(y_test, "b", label="Original Price")
        plt.plot(y_predicted, "r", label="Predicted Price")
        plt.title(f"Final Prediction for {ticker}")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()
        plot_img_final_prediction = save_plot(f"{ticker}_final_prediction_plot.png")

        # ---------- Metrics ----------
        mse = mean_squared_error(y_test, y_predicted)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(y_test, y_predicted)

        return Response(
            {
                "status": "success",
                "plot_img": plot_img,
                "plot_img_ma": plot_img_ma,
                "plot_img_ma200": plot_img_ma200,
                "plot_img_final_prediction": plot_img_final_prediction,
                "mse": float(mse),
                "rmse": rmse,
                "r2": float(r2),
            }
        )
