// import React from 'react'
import { Link } from "react-router-dom";
import notebook from '../assets/Side image.png'
import '../css/Welcome.css'

const Welcome = () => {
    return (
        <div className="welcome basic-page">

            <div className='welcome__info'>
                <div style={{ position: "relative" }}>
                    <svg
                        width="800"
                        height="800"
                        viewBox="0 0 800 800"
                        style={{
                        position: "absolute",
                        top: "-250px",    // ниже
                        right: "-200px",
                        zIndex: -1,
                        }}
                    >
                        <defs>
                        <filter id="blurOval">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="60" />
                        </filter>
                        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                            <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                        </linearGradient>
                        </defs>
                        <ellipse
                        cx="400"
                        cy="400"
                        rx="300"
                        ry="200"
                        fill="url(#grad)"
                        filter="url(#blurOval)"
                        />
                    </svg>
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
                    <svg
                        width="1000"
                        height="1000"
                        viewBox="0 0 1000 1000"
                        style={{
                        position: "absolute",
                        bottom: "-100px",    // ниже
                        left: "100px",
                        zIndex: -1,
                        }}
                    >
                        <defs>
                        <filter id="blurOval">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="60" />
                        </filter>
                        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                            <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                        </linearGradient>
                        </defs>
                        <ellipse
                        cx="500"
                        cy="500"
                        rx="300"
                        ry="200"
                        fill="url(#grad)"
                        filter="url(#blurOval)"
                        />
                    </svg>
                </div>
                <img src={notebook} alt="" />
            </div>



        </div>
    )
}

export default Welcome