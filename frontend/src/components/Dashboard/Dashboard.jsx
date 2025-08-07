import { useEffect, useState } from 'react'
import axiosInstance from '../../axiosInstance'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

const Dashboard = () => {
    const [ticker, setTicker] = useState('');
    const [error, setError] = useState();
    const [loading, setLoading] = useState(false);
    const [plot, setPlot] = useState(null);
    const [plotMa, setPlotMa] = useState(null);
    const [plotMa200, setPlotMa200] = useState(null);
    const [plotPredictionUrl, setPlotPredictionUrl] = useState(null);
    const [mse, setMse] = useState(null);
    const [rmse, setRmse] = useState(null);
    const [r2, setR2] = useState(null);

    useEffect(() => {
        const fetchProtectedData = async () => {
            try {
                const response = await axiosInstance.get('/protected-view/');
            } catch(error) {
                console.error('Error fetching data: ', error);
            }
        }
        fetchProtectedData();
    }, [])

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await axiosInstance.post('/predict/', { ticker: ticker });
            const backendRoot = import.meta.env.VITE_BACKEND_ROOT;
            const plotUrl = `${backendRoot}${response.data.plot_img}`
            const plotMaUrl = `${backendRoot}${response.data.plot_img_ma}`;
            const plotMa200Url = `${backendRoot}${response.data.plot_img_ma200}`;
            const plotPredictionUrl = `${backendRoot}${response.data.plot_img_final_prediction}`;

            // Set metrics
            setMse(response.data.mse);
            setRmse(response.data.rmse);
            setR2(response.data.r2);

            // Set plots
            setPlot(plotUrl);
            setPlotMa(plotMaUrl);
            setPlotMa200(plotMa200Url)
            setPlotPredictionUrl(plotPredictionUrl);

            if (response.data.error) {
                setError(response.data.error);
            }
        } catch (error) {
            console.error('Error submitting ticker: ', error);
        } finally {
            setLoading(false);
        }
    };

  return (
    <div className="container">
        <div className="row">
            <div className="col-md-6 mx-auto">
                <form onSubmit={handleSubmit}>
                    <input type="text" className="form-control" placeholder="Enter Stock Ticker" onChange={(e) => setTicker(e.target.value)} required/>
                    <small>{error && <div className='text-danger'>{error}</div>}</small>
                    <button type='submit' className='btn btn-info mt-3'>
                        { loading ? <span><FontAwesomeIcon icon={faSpinner} spin /> Please wait...</span> : 'Predict Stock Price' }
                    </button>
                </form>
            </div>

            {/* Display the plot if it exists */}
            {plotPredictionUrl && (
              <div className="prediction mt-5">
                <div className="p-3">
                    {plot && (
                        <img src={plot} style={{maxWidth: '100%'}}/>
                    )}
                </div>
                <div className="p-3">
                    {plotMa && (
                        <img src={plotMa} style={{maxWidth: '100%'}}/>
                    )}
                </div>
                <div className="p-3">
                    {plotMa200 && (
                        <img src={plotMa200} style={{maxWidth: '100%'}}/>
                    )}
                </div>
                <div className="p-3">
                    {plotPredictionUrl && (
                        <img src={plotPredictionUrl} style={{maxWidth: '100%'}}/>
                    )}
                </div>
                <div className="text-light p3">
                    <h4>
                        Model Evaluation
                    </h4>
                    <p>Mean Squared Error (MSE): {mse}</p>
                    <p>Root Mean Squared Error (RMSE): {rmse}</p>
                    <p>R-Squared (R2): {r2}</p>
                </div>
            </div>  
            )}
        </div>
    </div>
  )
}

export default Dashboard;