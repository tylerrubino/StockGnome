import React from 'react'
import Button from './Button'
import Header from './Header'
import Footer from './Footer'

const Main = () => {
  return (
    <>
        {/* <div className="container">
            <div className='p-5 text-center bg-light-dark rounded'>
                <h1 className='text-light'>Let the Gnome Crunch the Numbers.</h1>
                <p className="text-light lead">A full-stack web app built with Django, React, and a custom-trained machine learning model to forecast future stock prices. Users can visualize predictions, analyze historical trends, and interact with intelligent market insights—all in one intuitive dashboard.</p>
                <Button text='Login' class='btn-outline-info' url='/login'/>
            </div>local
        </div> */}
         (
    <main className="container text-light py-5">
      {/* HERO SECTION */}
      <section className="text-center mb-5">
        <img src="../../public/StockGnomeClear.png" className="hero-icon mb-4" alt="StockGnome Logo" />
        <h1 className="display-4 font-weight-bold mb-3">Let the Gnome Crunch the Numbers</h1>
        <p className="lead mb-4">
          StockGnome is an AI-powered platform that predicts future stock prices and trends using machine learning and real-time analytics.
        </p>
        <Button text="Get Started" class="btn-glow btn-outline-info btn-lg px-4" url="/login" />
      </section>

      {/* HOW IT WORKS */}
      <section className="row my-5 align-items-center">
        <div className="col-md-6 mb-4 mb-md-0">
          <h2 className="font-weight-bold">How It Works</h2>
          <p>
            We train custom ML models on historical market data, sentiment signals, and macroeconomic indicators. 
            Every forecast is computed using a blend of regression techniques and time series analysis.
          </p>
          <p>
            Our stack: <strong>Django</strong> (Python backend), <strong>React</strong> (interactive UI), and <strong>PostgreSQL</strong> (secure storage).
          </p>
        </div>
        <div className="col-md-6 text-center">
          <img src="/static/images/forecast-preview.png" className="img-fluid rounded shadow" alt="Forecast Graph" />
        </div>
      </section>

      {/* WHY IT MATTERS */}
      <section className="my-5 text-center">
        <h2 className="font-weight-bold mb-4">Why Use StockGnome?</h2>
        <div className="row">
          <div className="col-md-4 mb-4">
            <h5>📈 Smarter Investing</h5>
            <p>Make informed decisions using forward-looking data, not gut feelings.</p>
          </div>
          <div className="col-md-4 mb-4">
            <h5>⚙️ Powerful Automation</h5>
            <p>Our models continuously learn and adapt as new data arrives.</p>
          </div>
          <div className="col-md-4 mb-4">
            <h5>🧠 Intuitive Insights</h5>
            <p>Clean, readable dashboards surface only what matters—no clutter.</p>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="my-5">
        <h2 className="font-weight-bold text-center mb-4">Core Features</h2>
        <div className="row text-center">
          <div className="col-md-3 mb-4">
            <h6>📊 Price Forecasting</h6>
            <p>AI-powered price predictions for short- and medium-term timelines.</p>
          </div>
          <div className="col-md-3 mb-4">
            <h6>📉 Historical Analysis</h6>
            <p>Overlay historical performance to validate forecasts.</p>
          </div>
          <div className="col-md-3 mb-4">
            <h6>💬 Intelligent Commentary</h6>
            <p>Natural language summaries generated with ML models.</p>
          </div>
          <div className="col-md-3 mb-4">
            <h6>🔒 Private & Secure</h6>
            <p>Built on secure open-source frameworks with strong data protection.</p>
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="text-center my-5">
        <h2 className="font-weight-bold mb-3">Ready to See the Future?</h2>
        <p className="mb-4">Sign in now to explore the dashboard and forecast your first stock.</p>
        <Button text="Login" class="btn-outline-info btn-lg px-4 mr-3" url="/login" />
        &nbsp;
        <Button text="Register" class="btn-info btn-lg px-4" url="/register" />
      </section>
    </main>
    </>
  )
}

export default Main