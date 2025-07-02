import React, { useState } from "react";
import TrainingEditor from "../components/CourseEditor";
import Metadata from "../components/Metadata";
import "../css/UploadTrainingPage.css";
import { Link } from "react-router-dom";

interface StepData {
    [key: string]: any;
}

const UploadTrainingPage = () => {

    const [step, setStep] = useState<"welcome" | "metadata" | "editor" | "end">("welcome");

    const [savedData, setSavedData] = useState<StepData>({
        activity_type: "",
        program_goal: [],
        training_environment: [],
        difficulty_level: "",
        course_duration: 0,
        weekly_training_frequency: "",
        average_workout_duration: "",
        age_group: [],
        gender_orientation: "",
        physical_limitations: [],
        required_equipment: [],
        course_language: "",
        visual_content: [],
        trainer_feedback_options: [],
        tags: [],
        trainer_name: "",
        course_title: "",
        program_description: "",
        training_plan: []
    });

    const handleSubmit = () => {
        console.log("Saved data: ", savedData);
        // Можно передать savedData в TrainingEditor здесь
        setStep("end");
    };

    const nextStep = () => {
        if (step === "welcome") setStep("metadata");
        else if (step === "metadata") setStep("editor");
    };

    const prevStep = () => {
        if (step === "editor") setStep("metadata");
        else if (step === "metadata") setStep("welcome");
    };

    return (
        <div className="basic-page">
            <div>
                {step === "welcome" && (
                <div className="centered-content">

                    <div className="step-title-main">Welcome to the Training Course Creator</div>
                    <p>Let’s help you design a personalized fitness program from scratch.</p>
                    <button className="btn-basic-black" onClick={nextStep}>Get Started</button>
                </div>
                )}

                {step === "metadata" && (
                <div className="metadata-content">
                    <Metadata 
                        savedData={savedData} 
                        setSavedData={setSavedData}
                        onNext={nextStep}
                        onBack={prevStep} 
                    />
                </div>
                )}

                {step === "editor" && (
                <>
                
                    <TrainingEditor 
                    savedData={savedData} 
                    setSavedData={setSavedData}
                    onBack={prevStep}
                    onSubmit={handleSubmit}
                    />
                </>
                )}

                {step === "end" && (
                <div className="centered-content">
                    <div className="step-title-main">New training plan was succesfully created!</div>
                    <p>You can view it or return to the main page, as you wish.</p>
                    <div className="buttons">
                        <button className="btn-basic-black"><Link to="/">View plan</Link></button>
                        <button className="btn-basic-white"><Link to="/">Main menu</Link></button>
                    </div>
                </div>
                )}
            </div>
        </div>
    );
};

export default UploadTrainingPage;