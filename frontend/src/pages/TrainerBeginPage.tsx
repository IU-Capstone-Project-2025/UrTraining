// import React from 'react'
import '../css/BeginPage.css'
import Begin from "../components/Begin"

const TrainerBeginPage = () => {
    const textProps = {
        title: "Turn your experience into impact.",
        description: `Whether you're a seasoned pro or just starting out,
                        UrTraining lets you create structured workouts, reach new clients,
                        and grow your coaching presence — all in one place.`,
        button_1: "Upload first training",
        button_2: "Grow your audience",
        button_3: "Monetize your expertise"
    };

    return (
        <>
            <Begin css_style="begin__left" text={textProps}/>
        </>
    )
}

export default TrainerBeginPage