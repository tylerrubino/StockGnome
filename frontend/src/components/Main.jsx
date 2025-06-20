import React from 'react'
import Button from './Button'

const Main = () => {
  return (
    <>
        <div className="container">
            <div className='p-5 text-center bg-light-dark rounded'>
                <h1 className='text-light'>Let the Gnome Crunch the Numbers.</h1>
                <p className="text-light lead">A full-stack web app built with Django, React, and a custom-trained machine learning model to forecast future stock prices. Users can visualize predictions, analyze historical trends, and interact with intelligent market insights—all in one intuitive dashboard.</p>
                <Button text='Login' class='btn-outline-info'/>
            </div>local
        </div>
    </>
  )
}

export default Main