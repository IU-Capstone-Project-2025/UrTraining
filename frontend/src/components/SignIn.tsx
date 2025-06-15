// import React from 'react'
import '../css/SingUp.css'
import SignUp_Image from '../assets/signup_image.jpg'

const SignIn = () => {
    return (
        <div className="signup basic-page">
            <div className='signup__container'>
                <div className='signup__image'>
                    <img src={SignUp_Image} alt="" />
                </div>
                <div className='signup__form-area'>
                    <h2 className='signup__form-area__title'>
                        Welcome back!
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
                            id="password"
                            name="password"
                            className='form-basic-white'
                            placeholder="Password"
                        />

                        <input
                            type="submit"
                            value="Sign In"
                            className='btn-basic-black'
                        ></input>
                    </form>
                    <div className='signup__form-area__divider'></div>
                    <div className='signup__form-area__social'>
                        <button className='btn-basic-white'>
                            Sign In with Google
                        </button>
                        <button className='btn-basic-white'>
                            Sign In with Telegram
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignIn