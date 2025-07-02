import React from 'react'
import kanye from '../assets/kanye.jpg'
import arrow from '../assets/arrow.svg'
import '../css/Profile.css'

const Profile = () => {
    return (
        <div className='profile basic-page'>
            <div className='profile__container'>
                <div className='profile__frame profile__info'>
                    <div className='profile__info__header'>
                        <button className='btn-basic-white profile__header__logout'>
                            Log out
                        </button>
                    </div>
                    <div className='profile__info__avatar'>
                        <img src={kanye} alt="kanye" />
                    </div>
                    <div className='profile__info__desc'>
                        <h3>trainerOne</h3>
                        <p>trainer</p>
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
                                <h3>E-mail</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>y.ye@mail.ru</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Gender</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>Male</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Age</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>40</p>
                            </div>
                        </div>
                        <div className='profile__personal__field'>
                            <div className='profile__field__name'>
                                <h3>Tags</h3>
                            </div>
                            <div className='profile__field__value'>
                                <p>Cardio, HIIT, Yoga, Functional
                                    trainings, Stretching</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='profile__frame profile__calendar'>
                    <div className='profile__calendar__date'>
                        <h3>Today is 11 September 2001</h3>
                    </div>
                    <div className='profile__calendar__option'>
                        <p>Ready to lead the way today? Your athletes are waiting!</p>
                        <button className='btn-basic-white'>See the statistics</button>
                    </div>
                    <div className='profile__calendar__option'>
                        <p>You can discover the programs of other trainers or create your own:</p>
                        <button className='btn-basic-black'>View all plans</button>
                    </div>
                </div>
                <div className='profile__frame profile__trainings'>
                    <div className='profile__trainings__header'>
                        <p>Have some new ideas on paper?</p>
                        
                    </div>
                    <div className='profile__trainings__footer'>
                        <h3>Upload new training plan now</h3>
                    </div>
                </div>
                <div className='profile__frame profile__upload'>
                    <div className='profile__upload__button'>
                        <button className='btn-basic-black'>View my trainings</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Profile