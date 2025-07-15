// import React from 'react'
import { Link } from "react-router-dom";
import notebook from '../assets/Side image.png'
import '../css/Welcome.css'

const Welcome = () => {
    return (
        <div className="welcome basic-page">

            <svg style={{ position: 'absolute', width: 0, height: 0 }}>
                <filter id="blurOval" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="60" />
                </filter>
            </svg>

            <div className='welcome__info'>
                <div style={{ position: "relative" }}>
                    <div className="assets__background__gradient" 
                    style={{ 
                        top: "0", 
                        right: "0", 
                        background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                        filter: 'url(#blurOval)',
                    }}>
                    </div>
                </div>

                <div className='welcome__info__text'>
                    <h1>
                        Smart approach to training powered by AI
                    </h1>
                    <h3>
                        Create and share your training programs as a coach faster.
                        Get AI—personalized workouts based on your goals and condition as user —
                        all in one place
                    </h3>
                </div>
                <div className='welcome__info__buttons'>
                    <Link to={"/trainee-begin"}>
                        <button className='btn-basic-blur'>
                            I want to train
                        </button>
                    </Link>
                    <Link to={"/trainer-begin"}>
                        <button className='btn-basic-black'>
                            I am a Coach
                        </button>
                    </Link>
                </div>
            </div>

            <div className="welcome__image__container">
                <div style={{ position: "relative" }}>
                    <div className="assets__background__gradient" 
                    style={{ 
                        top: "0", 
                        left: "0", 
                        background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                        filter: 'url(#blurOval)',
                    }}>
                    </div>
                </div>
                <img src={notebook} alt="" />
            </div>



        </div>
    )
}

export default Welcome