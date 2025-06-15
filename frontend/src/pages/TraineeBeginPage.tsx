// import React from 'react'
import '../css/BeginPage.css'
import Begin from "../components/Begin"

const TraineeBeginPage = () => {
    const textProps = {
        title: "Workouts made for you. Instantly.",
        description: `Tell us about yourself — your age, fitness level, goals, and preferences
                        — and let AI build a personalized training plan for you.
                        No generic programs. Just what works for you, updated as you grow.`,
        button_1: "Tell us yor goals",
        button_2: "Receive smart plans",
        button_3: "Start today"
    };

    return (
        <>
            <Begin css_style="begin__right" text={textProps}/>
        </>
    )
}

export default TraineeBeginPage