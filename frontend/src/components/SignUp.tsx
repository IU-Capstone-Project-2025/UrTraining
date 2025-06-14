// import React from 'react'
import '../css/SingUp.css'
import SignUp_Image from '../assets/signup_image.jpg'

const SignUp = () => {
    return (
        <div className="signup basic-page">
            <div className='signup__container'>
                <div className='signup__image'>
                    <img src={SignUp_Image} alt="" />
                </div>
                <div className='signup__form-area'>
                    <h2 className='signup__form-area__title'>
                        Sign Up
                    </h2>
                    <form className='signup__form-area__options'>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            className='form-basic-white'
                            placeholder="Username"
                        />
                        <input
                            type="text"
                            id="email"
                            name="email"
                            className='form-basic-white'
                            placeholder="Email"
                        />
                        <input
                            type="text"
                            id="password"
                            name="password"
                            className='form-basic-white'
                            placeholder="Password"
                        />
                        <label
                            style={{ display: "flex", alignItems: "baseline" }}
                        >
                            <input
                                type="checkbox"
                                id="agreement"
                                name="agreement"
                                className='checkbox-basic-white'
                                value="Boat"
                            ></input>
                            <p style={{ marginLeft: "8px" }}>
                                You agree with our Terms of Service
                            </p>
                        </label>

                        <input
                            type="submit"
                            value="Let's start!"
                            className='btn-basic-black'
                        ></input>
                    </form>
                    <div className='signup__form-area__divider'></div>
                    <div className='signup__form-area__social'>
                        <button className='btn-basic-white'>
                            Sign Up with Google
                        </button>
                        <button className='btn-basic-white'>
                            Sign Up with Telegram
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignUp