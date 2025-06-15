// import React from 'react'
import { Link } from "react-router-dom";
import '../css/Welcome.css'

const Welcome = () => {
    return (
        <div className="welcome basic-page">
            <div className='welcome__info'>
                <div className='welcome__info__text'>
                    <h1>
                        Smart approach to training with AI assistant
                    </h1>
                    <h3>
                        Create and share your training programs as a coach faster.
                        Get AI—personalized workouts based on your goals and condition as user —
                        all in one place
                    </h3>
                </div>
                <div className='welcome__info__buttons'>
                    <button className='btn-basic-white'>
                        <Link to={"/trainee-begin"}>
                            I want to train
                        </Link>
                    </button>
                    <button className='btn-basic-black'>
                        <Link to={"/trainer-begin"}>
                            I am a Coach
                        </Link>
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Welcome