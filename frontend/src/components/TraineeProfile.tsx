import React, { useContext } from 'react'
import kanye from '../assets/kanye.jpg'
import arrow from '../assets/arrow.svg'
import '../css/Profile.css'
import { logOutRequest } from '../api/apiRequests'
import { useNavigate } from 'react-router-dom'
import AuthContext from './context/AuthContext'
import TrainingCalendar from './TrainingCalendar';


const TraineeProfile = (data: any) => {

    const authData = useContext(AuthContext)
    const navigate = useNavigate();
    const today = new Date();
    const formattedCurrentDate = today.toLocaleDateString('ru-RU');

    const grid_template = "'" + data.grid_template.join("' '") + "'"

    const handleLogout = async () => {
        try {
            await logOutRequest(authData.access_token);
            
            localStorage.removeItem('token');
            
            navigate("/signin");
        } catch (error) {
            console.error('Ошибка при выходе:', error);
        }
    }

    return (
        <div className='profile basic-page'>
            
            <div style={{ position: "relative" }}>
                <svg
                    width="1200"
                    height="1200"
                    viewBox="0 0 1200 1200"
                    style={{
                        position: "absolute",
                        top: "-400px",
                        right: "-500px",
                        zIndex: -1,
                        pointerEvents: "none"
                    }}
                    >
                    <defs>
                        <filter
                        id="blurOval"
                        x="-50%"
                        y="-50%"
                        width="200%"
                        height="200%"
                        filterUnits="objectBoundingBox"
                        >
                        <feGaussianBlur in="SourceGraphic" stdDeviation="80" />
                        </filter>

                        <linearGradient id="grad" x1="0%" y1="100%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                        <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                        </linearGradient>
                    </defs>

                    <ellipse
                        cx="600"
                        cy="600"
                        rx="300"
                        ry="200"
                        fill="url(#grad)"
                        filter="url(#blurOval)"
                    />
                </svg>
            </div>

            <div style={{ position: "relative" }}>
                <svg
                    width="1600"
                    height="1600"
                    viewBox="0 0 1600 1600"
                    style={{
                    position: "absolute",
                    top: "-200px",    // ниже
                    left: "-600px",
                    zIndex: -1,
                    }}
                >
                    <defs>
                    <filter id="blurOval">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="60" />
                    </filter>
                    <linearGradient id="grad" x1="0%" y1="100%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                        <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                    </linearGradient>
                    </defs>
                    <ellipse
                    cx="800"
                    cy="800"
                    rx="300"
                    ry="200"
                    fill="url(#grad)"
                    filter="url(#blurOval)"
                    />
                </svg>
            </div>

            <div className='profile__container trainee-template'>
                <div className='profile__frame profile__info'>
                    <div className='profile__info__header'>
                        <button className='btn-basic-white profile__header__logout' onClick={handleLogout}>
                            Log out
                        </button>
                    </div>
                    <div className='profile__info__avatar'>
                        <img src={kanye} alt="kanye" />
                    </div>
                    <div className='profile__info__desc'>
                        <h3>{data.username}</h3>
                        <p>{data.user_type}</p>
                    </div>
                </div>
                <div className='profile__frame profile__personal'>
                    <div className='profile__personal__header'>
                        <h3>
                            Personal information
                        </h3>
                        <button className='btn-basic-white profile__personal__edit'>
                            Edit
                        </button>
                    </div>
                    <div className='profile__personal__fields'>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Full name</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>{data.full_name}</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>E-mail</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>{data.email}</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Gender</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>{data.gender}</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Age</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>{data.age}</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Tags</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>{data.tags.map((tag: string, index: number) => {
                                    return tag + (index === data.tags.length - 1 ? "" : ", ")
                                })}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='profile__frame profile__calendar'>
                    <div className='profile__calendar__date'>
                        <h3>Today is {data.date}</h3>
                    </div>
                    <div className='profile__calendar__option'>
                        <p>{data.calendar_text.text_top}</p>
                        <TrainingCalendar
                            schedule={data.schedule}
                            onDateClick={(date: String) => navigate(`/calendar/${date}`)}
                        />
                    </div>                    
                </div>

                <div className='profile__frame profile__today' onClick={() => navigate(`/calendar/${formattedCurrentDate}`)}>
                    <div className='profile__today__option'>
                        <p>{data.today_text.text_top}</p>
                        <button className='btn-basic-black'>{data.today_text.text_button}</button>
                    </div>
                </div>

                <div className='profile__frame profile__trainings' onClick={() => navigate("/saved-trainings")}>
                    <div className='profile__trainings__header'>
                        <p>{data.trainings_text.text_top}</p>
                        <img src={arrow} alt="" />
                    </div>
                    <div className='profile__trainings__footer'>
                        <h3>{data.trainings_text.text_bottom}</h3>
                    </div>
                </div>

                <div className='profile__frame profile__upload'>

                    <div className='profile__calendar__option'>
                        <p>{data.calendar_text.text_bottom}</p>
                        <button className='btn-basic-black' onClick={() => navigate("/catalogue")}>{data.calendar_text.text_button_top}</button>
                    </div>            
                    <div className='profile__calendar__option'>
                        <button className='btn-basic-white' onClick={() => navigate("/recommendations")}>{data.calendar_text.text_button_bottom}</button>
                    </div>
                    <div className='profile__upload__text'>
                        <p>{data.upload_text.text_top}</p>
                    </div>
                    <div className='profile__upload__button'>
                        <button className='btn-basic-black' onClick={() => navigate("/survey")}>{data.upload_text.text_button}</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TraineeProfile