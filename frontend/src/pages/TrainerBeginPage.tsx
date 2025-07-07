// import React from 'react'
import '../css/BeginPage.css'
import Begin from "../components/Begin"
import { useContext } from 'react';
import AuthContext from '../components/context/AuthContext';

const TrainerBeginPage = () => {
    const authData = useContext(AuthContext)

    const textProps = {
        title: "Turn your experience into impact.",
        description: `Whether you're a seasoned pro or just starting out,
                        UrTraining lets you create structured workouts, reach new clients,
                        and grow your coaching presence — all in one place.`,
        button_text: "Upload first training",
        // button_2: "Grow audience",
        // button_3: "Monetize expertise"
    };

    const componentProps = {
        css_style: "begin__left",
        button_link: authData.access_token === "" ? "/signup?role=trainer" : "/trainer-registration",
        text: textProps,
    }

    return (
        <>
            <Begin {...componentProps}/>
        </>
    )
}

export default TrainerBeginPage