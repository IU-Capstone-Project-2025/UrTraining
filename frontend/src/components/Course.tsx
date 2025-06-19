// import React from 'react'
import '../css/Course.css'
import kanye from '../assets/kanye.jpg'

const Course = () => {

    const day_1_data = [
        ["Cat-Cow Stretch", "10-12", "2", "", "30 sec", "Description"],
        ["Shoulder Rolls + Arm Swings", "20/2", "2", "", "20 sec", "Description"],
        ["Hip Circles", "10/2", "2", "", "20 sec", "Description"],
        ["Deep Squat Hold + Spinal Twist", "", "2", "30 sec", "30 sec", "Description"],
        ["Standing Hamstring Reach + Back Stretch", "", "2", "30 sec", "30 sec", "Description"],
        ["Dynamic Lunge with Reach", "10/2", "2", "", "30 sec", "Description"],
        ["Neck Mobility (Tilt, Turn, Nod)", "10", "1", "", "", "Description"],
    ];

    return (
        <div className="course basic-page">
            <div className="course__container">
                <div className='course__tags'>
                    <div className='course__tags__type'>
                        <div className='course__tag tag-basic-gray'>
                            <p>Mobility</p>
                        </div>
                    </div>
                    <div className='course__tags__intensity'>
                        <div className='course__tag tag-basic-gray'>
                            <p>for all levels</p>
                        </div>
                        <div className='course__tag tag-basic-gray'>
                            <p>30 min/training</p>
                        </div>
                        <div className='course__tag tag-basic-gray'>
                            <p>3-4 trainings/week</p>
                        </div>
                        <div className='course__tag tag-basic-gray'>
                            <p>2 weeks</p>
                        </div>
                    </div>
                    <div className='course__tags__requirement'>
                        <div className='course__tag tag-basic-gray'>
                            <p>No equipment</p>
                        </div>
                    </div>
                </div>

                <div className='course__info'>
                    <div className='course__info__title'>
                        <div className='course__info__name'>
                            <h2>Mobility reset</h2>
                        </div>
                        <div className='course__info__author'>
                            <h3>by trainerOne</h3>
                        </div>
                        <div className='course__info__reviews'>
                            <p>
                                4/5
                            </p>
                        </div>
                    </div>
                    <div className='course__info__description'>
                        <p>A short but effective mobility reboot.
                            This program is designed to help you restore natural joint range of motion,
                            improve flexibility, and reduce daily discomfort from sitting or inactivity.
                            No matter your fitness background, this program is a perfect reset button for your body.
                            view detailed info</p>
                    </div>
                </div>

                <div className='course__structure'>
                    <div className='course__structure__header'>
                        <h3>Course Structure</h3>
                        <div className='course__structure__options'>
                            <p>Option 1</p>
                            <p>Option 2</p>
                        </div>
                    </div>

                    <div className='course__structure__container'>
                        <div className='course__structure__session'>
                            <div className='course__session__table'>
                                <div className='course__session__title'>
                                    <h2>
                                        Monday session
                                    </h2>
                                </div>
                                <div className='course__table__header'>
                                    {["Exercise", "Reps", "Sets", "Duration", "Rest", "Description"]
                                        .map(h => <div key={h} className="course__table__cell">{h}</div>)}
                                </div>
                                <div className='course__table__body'>
                                    {day_1_data.map((row, i) => (
                                        <div key={i} className="course__table__row">
                                            {row.map((c, j) => <div key={j} className="course__table__cell">{c || "-"}</div>)}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className='course__structure__session'>
                            <div className='course__session__table'>
                                <div className='course__session__title'>
                                    <h2>
                                        Monday session
                                    </h2>
                                </div>
                                <div className='course__table__header'>
                                    {["Exercise", "Reps", "Sets", "Duration", "Rest", "Description"]
                                        .map(h => <div key={h} className="course__table__cell">{h}</div>)}
                                </div>
                                <div className='course__table__body'>
                                    {day_1_data.map((row, i) => (
                                        <div key={i} className="course__table__row">
                                            {row.map((c, j) => <div key={j} className="course__table__cell">{c || "-"}</div>)}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className='course__coach'>
                    <div className='course__coach__title'>
                        <h2>About coach:</h2>
                    </div>
                    <div className='course__coach__picture'>
                        <img src={kanye} alt="pfp" />
                    </div>
                    <div className='course__coach__info'>
                        <div className='course__coach__name'>
                            <h2>trainerOne</h2>
                        </div>
                        <div className='course__coach__statistics'>
                            <p>12 active training courses</p>
                            <p>4,100 views</p>
                        </div>
                        <div className='course__coach__tags'>
                            <div>
                                <p>#10 in Coaches Honor Roll</p>
                            </div>
                            <div>
                                <p>Certification approved</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Course