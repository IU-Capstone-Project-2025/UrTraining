import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { SignProps, InputField, SocialLink } from "./interface/interfaces";
import { useAuth } from '../context/AuthContext';
import '../css/Sing.css'

const Sign = (props: SignProps) => {
    const navigate = useNavigate();
    const { login, register } = useAuth();
    const [formData, setFormData] = useState<{ [key: string]: string }>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>('');

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (props.user_exists) {
                // Вход в систему
                await login(formData.username, formData.password);
                navigate('/');
            } else {
                // Регистрация
                await register(
                    formData.username,
                    formData.email,
                    formData.password,
                    formData.username // Используем username как full_name пока
                );
                navigate('/survey');
            }
        } catch (error: any) {
            setError(error.response?.data?.detail || 'Произошла ошибка');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="signup basic-page">
            <div className='signup__container'>
                <div className='signup__image'>
                    <img src={props.image_path} alt="" />
                </div>
                <div className='signup__form-area'>
                    <h2 className='signup__form-area__title'>
                        {props.page_title}
                    </h2>
                    {error && (
                        <div style={{ color: 'red', marginBottom: '10px', textAlign: 'center' }}>
                            {error}
                        </div>
                    )}
                    <form className='signup__form-area__options' onSubmit={handleSubmit}>
                        {props.input_fields.map((input: InputField, value: number) => {
                            return (
                                <input
                                    type={input.input_type}
                                    id={input.id}
                                    key={value}
                                    name={input.name}
                                    className='form-basic-white'
                                    placeholder={input.placeholder}
                                    value={formData[input.name] || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            );
                        })}
                        {!props.user_exists ?
                            <label
                                style={{ display: "flex", alignItems: "baseline" }}
                            >
                                <input
                                    type="checkbox"
                                    id="agreement"
                                    name="agreement"
                                    className='checkbox-basic-white'
                                    required
                                ></input>
                                <p style={{ marginLeft: "8px" }}>
                                    You agree with our Terms of Service
                                </p>
                            </label> :
                            <></>
                        }
                        <input
                            type="submit"
                            value={loading ? "Загрузка..." : "Let's start!"}
                            className='btn-basic-black'
                            disabled={loading}
                        ></input>
                    </form>
                    <div className='signup__form-area__divider'></div>
                    <div className='signup__form-area__social'>
                        {props.social_links.map((social: SocialLink, value: number) => {
                            return (<button key={value} className='btn-basic-white'>
                                {social.placeholder}
                            </button>);
                        })}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Sign