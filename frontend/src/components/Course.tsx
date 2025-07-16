// import React from 'react'
import '../css/Course.css'
import star from '../assets/star.svg'
import { useEffect, useRef, useState } from 'react';
import { saveProgram } from '../api/apiRequests';
import { Link } from 'react-router-dom';
import Dot from '../assets/Dot.svg'

interface Badge {
    badge_text: string;
    badge_color: string;
}

interface Exercise {
    exercise: string;
    repeats: string;
    sets: string;
    duration: string;
    rest: string;
    description: string;
}

interface TrainingDay {
    title: string;
    exercises: Exercise[];
}

interface CoachData {
    username: string;
    id: number;
    profile_picture: string;
    rating: number;
    reviews: number;
}

interface TrainingData {
    header_badges: {
        training_type: Badge[];
        training_info: Badge[];
        training_equipment: Badge[];
    };
    course_info: {
        title: string;
        author: string;
        description: string;
        rating: number;
        reviews: number;
    };
    training_plan: TrainingDay[];
    coach_data: CoachData;
    id: any;
}

type CourseProps = TrainingData & {
    savedStatus?: boolean;
    isCreated?: boolean;
    handleAddToSaved: () => void;
    handleDeleteFromSaved: () => void;
    handleDeleteTraining: () => void;
};

const Course: React.FC<CourseProps> = ({
    savedStatus,
    isCreated,
    handleAddToSaved,
    handleDeleteFromSaved,
    handleDeleteTraining,
    ...data
}) => {
    const scrollRef = useRef<HTMLDivElement>(null);
    const currentTrainerLink = `/catalogue/${data.coach_data.id}`;

    console.log(data);

    // Function for horizontal scroll
    // useEffect(() => {
    //     const scrollElement = scrollRef.current;
    //     if (!scrollElement) return;

    //     const onWheel = (e: WheelEvent) => {
    //         e.preventDefault();              // Prevent vertical page scroll
    //         scrollElement.scrollLeft += e.deltaY;      // Scroll horizontally instead
    //     };

    //     scrollElement.addEventListener('wheel', onWheel, { passive: false });
    //     return () => scrollElement.removeEventListener('wheel', onWheel);
    // }, []);

    return (
        <div className="course basic-page">

            <div style={{ position: "relative" }}>
                <svg
                    width="1200"
                    height="1200"
                    viewBox="0 0 1200 1200"
                    style={{
                        position: "absolute",
                        top: "300px",
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

                        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
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
                    width="1200"
                    height="1200"
                    viewBox="0 0 1200 1200"
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
                        cx="600"
                        cy="600"
                        rx="300"
                        ry="200"
                        fill="url(#grad)"
                        filter="url(#blurOval)"
                    />
                </svg>
            </div>

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
                            <Link to={currentTrainerLink} state={{ authorName: data.coach_data.username }}>
                                <div className='course__info__author'>
                                    <h3>by {data.course_info.author}</h3>
                                </div>
                            </Link>
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
                        {/* <div className='course__structure__options'>
                            <p>Option 1</p>
                            <p>Option 2</p>
                        </div> */}
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
                                        {training.exercises.map((exercise: any, index: number) => (
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

                    <div className='course__structure__container course__structure__mobile' ref={scrollRef}>
                        {data.training_plan.map((training: any, index: number) => (
                            <div key={index} className="course__structure__session">
                                <div className="course__session__table">
                                    <div className="course__session__title">
                                        <h2>{training.title}</h2>
                                    </div>

                                    <div className="course__table__body">
                                        {training.exercises.map((exercise: any, index: number) => (
                                            <div key={index} className="course__table__row">
                                                <div className="course__row__title">
                                                    <h3>
                                                        {(index + 1) + ". " + exercise.exercise}
                                                    </h3>
                                                </div>

                                                <div className="course__row__values">
                                                    <div className="course__row__info">
                                                        <p>{exercise.repeats === '-' ? 0 : exercise.repeats} reps</p>
                                                        <img src={Dot} alt="" style={{width: '0.4rem', height: '0.4rem'}} />
                                                        <p>{exercise.sets === '-' ? 0 : exercise.sets} sets</p>
                                                    </div>

                                                    <div className="course__row__rest">
                                                        <p>Time: {exercise.duration === '-' ? '0 sec' : exercise.duration}</p>
                                                        <p>Rest: {exercise.rest === '-' ? '0 sec' : exercise.rest} between sets</p>
                                                    </div>
                                                </div>

                                                <div className="course__row__description">
                                                    <h3>Description:</h3>
                                                    <p>{exercise.description}</p>
                                                </div>

                                                {/* {Object.entries(exercise).map(([key, value]: any) => (
                                                    <div key={key} className="course__table__cell">
                                                        {value}
                                                    </div>
                                                ))} */}
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
                    <Link to={currentTrainerLink} state={{ authorName: data.coach_data.username }}>
                        <div className='course__coach__info'>
                            <div className='course__coach__name'>
                                <h2>{data.coach_data.username}</h2>
                            </div>
                            <div className='course__coach__rating'>
                                <img src={star} alt="" />
                                <p>{data.coach_data.rating}/5</p>
                                <p>{data.coach_data.reviews} reviews</p>
                            </div>
                        </div>
                    </Link>
                </div>

                <div className='centered__content'>
                    <button className="btn-basic-black" onClick={() => {
                        if (savedStatus) {
                            handleDeleteFromSaved();
                        } else {
                            handleAddToSaved();
                        }
                    }}>
                        {savedStatus ? "Delete from saved" : "Save training"}
                    </button>
                    {isCreated === true && (
                        <button className="btn-basic-red" onClick={() => handleDeleteTraining()}>
                            Delete the training
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Course