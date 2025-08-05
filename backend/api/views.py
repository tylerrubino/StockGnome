from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import StockPredictionSerializer
from rest_framework.response import Response
from rest_framework import status
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score

# Create your views here.
class StockPredictionAPIView(APIView):
    """
    API View to handle stock predictions.
    """
    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            # Fetch the stock data from yfinance
            now = datetime.now()
            start = datetime(now.year-10, now.month, now.day)
            end = now
            df = yf.download(ticker, start=start, end=end)
            if df.empty:
                return Response({'error': 'No data found for the ticker', 'status': status.HTTP_404_NOT_FOUND})
            df = df.reset_index()

            # Generate Basic Plot
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.title('Stock Closing Price for {}'.format(ticker))
            plt.xlabel('Days')
            plt.ylabel('Close Price')
            plt.legend()

            # Save the plot to a file
            plot_img_path = f'{ticker}_plot.png'
            plot_img = save_plot(plot_img_path)
            
            # 100 Days Moving Average
            ma100 = df.Close.rolling(window=100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 Days Moving Average')
            plt.title('100 DMA for {}'.format(ticker))
            plt.xlabel('Days')
            plt.ylabel('Close Price')
            plt.legend()

            plot_img_path_ma = f'{ticker}_ma100_plot.png'
            plot_img_ma = save_plot(plot_img_path_ma)

            # 200 Days Moving Average
            ma200 = df.Close.rolling(window=200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(df.Close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 Days Moving Average')
            plt.plot(ma200, 'g', label='200 Days Moving Average')
            plt.title('200 DMA for {}'.format(ticker))
            plt.xlabel('Days')
            plt.ylabel('Close Price')
            plt.legend()

            plot_img_path_ma200 = f'{ticker}_ma200_plot.png'
            plot_img_ma200 = save_plot(plot_img_path_ma200)

            # Splitting data into Training and Testing data
            data_training = pd.DataFrame(df.Close[0:int(len(df)*0.70)])
            data_testing = pd.DataFrame(df.Close[int(len(df)*0.70): int(len(df))])

            # Scaling down the data between 0 and 1
            scaler = MinMaxScaler(feature_range=(0,1))

            # Load ML model
            model = load_model('stock_prediction_model.keras')

            # Preparing Test Data
            past_100_days = data_training.tail(100)
            final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
            input_data = scaler.fit_transform(final_df)
            x_test = []
            y_test = []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i-100:i])
                y_test.append(input_data[i, 0])
            x_test, y_test = np.array(x_test), np.array(y_test)

            # Making Predictions
            y_predicted = model.predict(x_test)

            # Revert the scaled prices to original prices
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

            # Plot the final prediction
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(y_test, 'b', label='Original Price')
            plt.plot(y_predicted, 'r', label='Predicted Price')
            plt.title('Final Prediction for {}'.format(ticker))
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()

            plot_img_path_final_prediction = f'{ticker}_final_prediction_plot.png'
            plot_img_final_prediction = save_plot(plot_img_path_final_prediction)

            # Model Evaluation
            # Mean Squared Error (MSE)
            mse = mean_squared_error(y_test, y_predicted)

            # Root Mean Squared Error (RMSE)
            rmse = np.sqrt(mse)

            # R^2 Score
            r2 = r2_score(y_test, y_predicted)

            return Response({
                'status': 'success', 
                'plot_img': plot_img, 
                'plot_img_ma': plot_img_ma, 
                'plot_img_ma200': plot_img_ma200, 
                'plot_img_final_prediction': plot_img_final_prediction,
                'mse': mse,
                'rmse': rmse,
                'r2': r2
                })