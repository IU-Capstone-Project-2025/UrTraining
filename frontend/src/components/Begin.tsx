import React from 'react';
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from '../context/AuthContext';

interface BeginProps {
    css_style: string;
    text: {
        title: string;
        description: string;
        button_1: string;
        button_2: string;
        button_3: string;
    };
}

const Begin = ({ css_style, text }: BeginProps) => {
    const { isAuthenticated, user } = useAuth();
    const navigate = useNavigate();

    const handleFirstButton = () => {
        // Если пользователь уже заполнял профиль, перенаправляем на главную
        if (isAuthenticated && user?.training_profile) {
            navigate('/');
        } else if (isAuthenticated) {
            // Если авторизован, но профиль не заполнен - на опрос
            navigate('/survey');
        } else {
            // Если не авторизован - на регистрацию
            navigate('/signup');
        }
    };

    const handleSecondButton = () => {
        // Показываем курсы
        if (isAuthenticated) {
            navigate('/');
        } else {
            navigate('/signin');
        }
    };

    const handleThirdButton = () => {
        // Начинаем тренировку
        if (isAuthenticated) {
            navigate('/course/example-course');
        } else {
            navigate('/signin');
        }
    };

    return (
        <div className={"begin basic-page " + css_style}>
            <div className="begin__container">
                <div className="begin__title">
                    <h1>
                        {text.title}
                    </h1>
                </div>
                <div className="begin__description">
                    <p>
                        {text.description}
                    </p>
                </div>
                <div className={"begin__buttons" + css_style}>
                    <button className="btn-basic-black" onClick={handleFirstButton}>
                            {text.button_1}
                        </button>
                    <button className="btn-basic-white" onClick={handleSecondButton}>
                        {text.button_2}
                    </button>
                    <button className="btn-basic-white" onClick={handleThirdButton}>
                        {text.button_3}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Begin