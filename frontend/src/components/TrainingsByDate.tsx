import React, { useRef } from 'react';
import '../css/TrainingsByDate.css';
import Dot from '../assets/Dot.svg';

import type { TrackerWithDataProp } from './interface/TrackerInterface';

type TrainingsByDateProps = {
    trainings: TrackerWithDataProp[];
};

const TrainingsByDate: React.FC<TrainingsByDateProps> = ({ trainings }) => {
    const scrollRef = useRef<HTMLDivElement>(null);

    return (
        <div className="trainings-by-date basic-page">

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
                        top: "-200px",
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

            <h1 className="trainings__title">
                <span style={{ display: 'block' }}>Trainings</span>
                <span style={{ display: 'block', marginBottom: '20px', opacity: '20%'}}>for the day</span>
            </h1>

            {trainings.length === 0 && (
                <p>No trainings scheduled for this date.</p>
            )}

            <div className="training__structure__container"  ref={scrollRef}>
                {trainings.map((training, index) => (
                    <div key={index} className="training__structure__session">
                        <h2 className="training__course-title">{training.course_title}</h2>
                        <h3 className="training__day-title" style={{ opacity: '30%'}}>{training.training_day.title}</h3>

                        <div className="training__table__header">
                            {["Exercise", "Reps", "Sets", "Duration", "Rest", "Description"].map((h) => (
                                <div key={h} className="course__table__cell">
                                    {h}
                                </div>
                            ))}
                        </div>

                        <div className="training__table__body">
                            {training.training_day.exercises.map((exercise, i) => (
                                <div key={i} className="training__table__row">
                                    <div className="training__table__cell">{exercise.exercise}</div>
                                    <div className="training__table__cell">{exercise.repeats}</div>
                                    <div className="training__table__cell">{exercise.sets}</div>
                                    <div className="training__table__cell">{exercise.duration}</div>
                                    <div className="training__table__cell">{exercise.rest}</div>
                                    <div className="training__table__cell">{exercise.description}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {/* Mobile View */}
            <div className="training__structure__container training__structure__mobile"  ref={scrollRef}>
                {trainings.map((training, index) => (
                    <div key={index} className="training__structure__session">
                        <h2 className="training__course-title">{training.course_title}</h2>
                        <h3 className="training__day-title" style={{ opacity: '30%'}}>{training.training_day.title}</h3>

                        {training.training_day.exercises.map((exercise, i) => (
                            <div key={i} className="training__table__row">
                                <div className="training__row__title">
                                    <h3>{i + 1}. {exercise.exercise}</h3>
                                </div>

                                <div className="training__row__values">
                                    <div className="training__row__info">
                                        <p>{exercise.repeats} reps</p>
                                        <img src={Dot} alt="dot" className="dot-separator" />
                                        <p>{exercise.sets} sets</p>
                                    </div>

                                    <div className="training__row__rest">
                                        <p>Time: {exercise.duration}</p>
                                        <p>Rest: {exercise.rest}</p>
                                    </div>
                                </div>

                                {exercise.description && (
                                    <div className="training__row__description">
                                        <h3>Description:</h3>
                                        <p>{exercise.description}</p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TrainingsByDate;
