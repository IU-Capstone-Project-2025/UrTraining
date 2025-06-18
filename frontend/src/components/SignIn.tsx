import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import '../css/SingUp.css'
import SignIn_Image from '../assets/singin_image.jpg'
import { authAPI } from '../utils/auth'
import type { LoginData } from '../utils/auth'
import { useAuth } from '../context/AuthContext'

const SignIn = () => {
    const [formData, setFormData] = useState<LoginData>({
        username: '',
        password: ''
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [successMessage, setSuccessMessage] = useState('')
    const navigate = useNavigate()
    const location = useLocation()
    const { login } = useAuth()

    useEffect(() => {
        // Check if there's a success message from registration
        if (location.state?.message) {
            setSuccessMessage(location.state.message)
            // Clear the state to prevent the message from persisting on page refresh
            window.history.replaceState({}, document.title)
        }
    }, [location])

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')
        setSuccessMessage('')

        try {
            const response = await authAPI.login(formData)
            
            // Update authentication context (this will immediately update navbar)
            login(response.access_token, response.user_info)
            
            // Navigate to appropriate begin page based on user role or to survey
            navigate('/trainee-begin')
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Login failed. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="signup basic-page">
            <div className='signup__container'>
                <div className='signup__image'>
                    <img src={SignIn_Image} alt="" />
                </div>
                <div className='signup__form-area'>
                    <h2 className='signup__form-area__title'>
                        Welcome back!
                    </h2>
                    {successMessage && (
                        <div style={{ 
                            color: 'green', 
                            backgroundColor: '#e8f5e8', 
                            padding: '10px', 
                            borderRadius: '4px', 
                            marginBottom: '15px',
                            border: '1px solid #c8e6c9'
                        }}>
                            {successMessage}
                        </div>
                    )}
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

                        <input
                            type="submit"
                            value={loading ? "Signing In..." : "Sign In"}
                            className='btn-basic-black'
                            disabled={loading}
                        />
                    </form>
                    <div className='signup__form-area__divider'></div>
                    <div className='signup__form-area__social'>
                        <button className='btn-basic-white' type="button" disabled>
                            Sign In with Google (Coming Soon)
                        </button>
                        <button className='btn-basic-white' type="button" disabled>
                            Sign In with Telegram (Coming Soon)
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignIn