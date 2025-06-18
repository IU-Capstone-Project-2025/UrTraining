import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../css/SingUp.css'
import SignUp_Image from '../assets/signup_image.jpg'
import { authAPI } from '../utils/auth'
import type { RegisterData } from '../utils/auth'

const SignUp = () => {
    const [formData, setFormData] = useState<RegisterData & { agreement: boolean }>({
        username: '',
        email: '',
        password: '',
        full_name: '',
        agreement: false
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }))
    }

    const validateForm = () => {
        if (formData.username.length < 3) {
            setError('Username must be at least 3 characters long')
            return false
        }
        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters long')
            return false
        }
        if (!formData.email.includes('@')) {
            setError('Please enter a valid email address')
            return false
        }
        if (formData.full_name.length < 2) {
            setError('Full name must be at least 2 characters long')
            return false
        }
        if (!formData.agreement) {
            setError('You must agree to the Terms of Service')
            return false
        }
        return true
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        if (!validateForm()) {
            setLoading(false)
            return
        }

        try {
            const registerData: RegisterData = {
                username: formData.username,
                email: formData.email,
                password: formData.password,
                full_name: formData.full_name
            }
            
            await authAPI.register(registerData)
            
            // Registration successful, navigate to sign in
            navigate('/signin', { 
                state: { message: 'Registration successful! Please sign in.' }
            })
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Registration failed. Please try again.')
        } finally {
            setLoading(false)
        }
    }

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
                    {error && (
                        <div style={{ 
                            color: 'red', 
                            backgroundColor: '#ffebee', 
                            padding: '10px', 
                            borderRadius: '4px', 
                            marginBottom: '15px',
                            border: '1px solid #ffcdd2'
                        }}>
                            {error}
                        </div>
                    )}
                    <form className='signup__form-area__options' onSubmit={handleSubmit}>
                        <input
                            type="text"
                            id="full_name"
                            name="full_name"
                            className='form-basic-white'
                            placeholder="Full Name"
                            value={formData.full_name}
                            onChange={handleInputChange}
                            required
                            disabled={loading}
                        />
                        <input
                            type="text"
                            id="username"
                            name="username"
                            className='form-basic-white'
                            placeholder="Username"
                            value={formData.username}
                            onChange={handleInputChange}
                            required
                            disabled={loading}
                        />
                        <input
                            type="email"
                            id="email"
                            name="email"
                            className='form-basic-white'
                            placeholder="Email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                            disabled={loading}
                        />
                        <input
                            type="password"
                            id="password"
                            name="password"
                            className='form-basic-white'
                            placeholder="Password"
                            value={formData.password}
                            onChange={handleInputChange}
                            required
                            disabled={loading}
                        />
                        <label
                            style={{ display: "flex", alignItems: "baseline" }}
                        >
                            <input
                                type="checkbox"
                                id="agreement"
                                name="agreement"
                                className='checkbox-basic-white'
                                checked={formData.agreement}
                                onChange={handleInputChange}
                                required
                                disabled={loading}
                            />
                            <p style={{ marginLeft: "8px" }}>
                                You agree with our Terms of Service
                            </p>
                        </label>

                        <input
                            type="submit"
                            value={loading ? "Creating Account..." : "Let's start!"}
                            className='btn-basic-black'
                            disabled={loading}
                        />
                    </form>
                    <div className='signup__form-area__divider'></div>
                    <div className='signup__form-area__social'>
                        <button className='btn-basic-white' type="button" disabled>
                            Sign Up with Google (Coming Soon)
                        </button>
                        <button className='btn-basic-white' type="button" disabled>
                            Sign Up with Telegram (Coming Soon)
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignUp