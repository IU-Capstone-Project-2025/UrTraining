// import React from 'react'
import '../css/Course.css'
import star from '../assets/star.svg'
import { useEffect, useRef } from 'react';

const Course = (data: any) => {
    const scrollRef = useRef<HTMLDivElement>(null);

    // Function for horizontal scroll
    useEffect(() => {
        const scrollElement = scrollRef.current;
        if (!scrollElement) return;

        const onWheel = (e: WheelEvent) => {
            e.preventDefault();              // Prevent vertical page scroll
            scrollElement.scrollLeft += e.deltaY * 4;      // Scroll horizontally instead
        };

        scrollElement.addEventListener('wheel', onWheel, { passive: false });
        return () => scrollElement.removeEventListener('wheel', onWheel);
    }, []);

    return (
        <div className="course basic-page">
            <div className="course__container">
                <div className='course__tags'>
                    {Object.entries(data.header_badges).map(([sectionKey, badges]: any) => (
                        <div
                            key={sectionKey}
                            className={`course__tags__type`}
                        >
                            {badges.map((badge: any, idx: any) => (
                                <div
                                    key={idx}
                                    className="course__tag tag-basic-gray"
                                    style={{ boxShadow: `inset 0px 0px 0px 1.5px ${badge.badge_color}`, color: badge.badge_color }}
                                >
                                    <p>{badge.badge_text}</p>
                                </div>
                            ))}
                        </div>
                    ))}
                </div>

                <div className='course__info'>
                    <div className='course__info__title'>
                        <div className='course__info__text'>
                            <div className='course__info__name'>
                                <h2>{data.course_info.title}</h2>
                            </div>
                            <div className='course__info__author'>
                                <h3>by {data.course_info.author}</h3>
                            </div>
                        </div>
                        <div className='course__info__reviews'>
                            <img src={star} alt="" />
                            <p>
                                {data.course_info.rating}/5
                            </p>
                            <p>
                                {data.course_info.reviews} reviews
                            </p>
                        </div>
                    </div>
                    <div className='course__info__description'>
                        <p>{data.course_info.description}</p>
                        <h4></h4>
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

                    <div className='course__structure__container' ref={scrollRef}>
                        {data.training_plan.map((training: any, index: number) => (
                            <div key={index} className="course__structure__session">
                                <div className="course__session__table">
                                    <div className="course__session__title">
                                        <h2>{training.title}</h2>
                                    </div>
                                    <div className="course__table__header">
                                        {["Exercise", "Reps", "Sets", "Duration", "Rest", "Description"]
                                            .map(h => (
                                                <div key={h} className="course__table__cell">
                                                    {h}
                                                </div>
                                            ))}
                                    </div>
                                    <div className="course__table__body">
                                        {training.exercises.map((exercise: any, value: number) => (
                                            <div key={index} className="course__table__row">
                                                {Object.entries(exercise).map(([key, value]: any) => (
                                                    <div key={key} className="course__table__cell">
                                                        {value}
                                                    </div>
                                                ))}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))
                        }
                    </div>
                </div>

                <div className='course__coach'>
                    <div className='course__coach__title'>
                        <h2>About coach:</h2>
                    </div>
                    <div className='course__coach__picture'>
                        <img src={data.coach_data.profile_picture} alt="pfp" />
                    </div>
                    <div className='course__coach__info'>
                        <div className='course__coach__name'>
                            <h2>{data.coach_data.username}</h2>
                        </div>
                        <div className='course__coach__rating'>
                            <img src={star} alt="" />
                            <p>{data.coach_data.rating}/5</p>
                            <p>{data.coach_data.reviews} reviews</p>
                        </div>
                        <div className='course__coach__statistics'>
                            <p>12 active training courses, </p>
                            <p>4,100 views</p>
                        </div>
                        <div className='course__coach__tags'>
                            <div>
                                <p>#10 in Coaches Honor Roll</p>
                            </div>
                            <div>
                                <p> Certification approved</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Course