// import React from 'react'
import '../css/Welcome.css'

const Welcome = () => {
    return (
        <div className="welcome-page basic-page">
            <div className='welcome-page_info'>
                <div className='welcome-page_info_text'>
                    <h1>Smart approach to training with AI assistant</h1>
                    <h3>Create and share your training programs as a coach faster. Get AI-personalized workouts based on your goals and condition as user — all in one place</h3>
                </div>
                <div className='welcome-page_info_buttons'>
                    <button className='btn-basic-white'>I Want to Train</button>
                    <button className='btn-basic-black'>I am a Coach</button>
                </div>
            </div>
        </div>
    )
}

export default Welcome