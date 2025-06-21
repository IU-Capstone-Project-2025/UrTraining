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
                    <Link to={"/trainee-begin"}>
                        <button className='btn-basic-white'>
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
        </div>
    )
}

export default Welcome