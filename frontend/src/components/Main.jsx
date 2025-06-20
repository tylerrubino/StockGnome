import React from 'react'
import Button from './Button'

const Main = () => {
  return (
    <>
        <div className="container">
            <div className='p-5 text-center bg-light-dark rounded'>
                <h1 className='text-light'>React-Django-Boilerplate</h1>
                <p className="text-light lead">A full-stack web application boilerplate using react + django.</p>
                <Button text='Login' class='btn-outline-info'/>
            </div>
        </div>
    </>
  )
}

export default Main