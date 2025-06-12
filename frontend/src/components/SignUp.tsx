// import React from 'react'
import '../css/SingUp.css'
import SignUp_Image from '../assets/signup_image.jpg'

const SignUp = () => {
    return (
        <div className="signup-section basic-page">
            <div className='signup-section_form'>
                <div className='signup-section_form_image'>
                    <img src={SignUp_Image} alt="" />
                </div>
                <div className='signup-section_form_input'>
                    <h2 className='signup-section_form_input_title'>Sign Up</h2>
                    <form className='signup-section_form_input_options'>
                        <input type="text" id="username" name="username" className='form-basic-white' placeholder="Username"/>
                        <input type="text" id="email" name="email" className='form-basic-white' placeholder="Email"/>
                        <input type="text" id="password" name="password" className='form-basic-white' placeholder="Password"/>
                        <label style={{ display: "flex", alignItems: "baseline" }}>
                            <input type="checkbox" id="agreement" name="agreement" className='checkbox-basic-white' value="Boat"></input>
                            <p style={{marginLeft: "8px"}}>You agree with our Terms of Service</p>
                        </label>
                        <input type="submit" value="Let's start!" className='btn-basic-black'></input>
                    </form>
                    <div className='signup-section_form_input_division'></div>
                    <div className='signup-section_form_input_other'>
                        <button className='btn-basic-white'>Sign Up with Google</button>
                        <button className='btn-basic-white'>Sign Up with Telegram</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignUp