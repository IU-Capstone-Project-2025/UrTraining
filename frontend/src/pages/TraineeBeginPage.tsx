// import React from 'react'
import '../css/BeginPage.css'
import Begin from "../components/Begin"
import { useContext } from 'react';
import AuthContext from '../components/context/AuthContext';

const TraineeBeginPage = () => {
    const authData = useContext(AuthContext)

    // Text data for element
    // Can be fetched from API or hardcoded
    const textProps = {
        title: "Workouts made for you. Instantly.",
        description: `Tell us about yourself — your age, fitness level, goals, and preferences
                        — and let AI build a personalized training plan for you.
                        No generic programs. Just what works for you, updated as you grow.`,
        button_text: "Tell us your goals",
        // button_2: "Smart plans",
        // button_3: "Start today"
    };

    const componentProps = {
        css_style: "begin__right",
        button_link: authData.access_token === "" ? "/signup" : "/survey",
        text: textProps,
    }

    return (
        <>
            <Begin {...componentProps}/>
        </>
    )
}

export default TraineeBeginPage