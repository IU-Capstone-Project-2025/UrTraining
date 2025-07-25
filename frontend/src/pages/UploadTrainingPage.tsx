import React, { useState, useContext, useEffect } from "react";
import TrainingEditor from "../components/CourseEditor";
import Metadata from "../components/Metadata";
import "../css/UploadTrainingPage.css";
import { Link, useNavigate } from "react-router-dom";
import AuthContext from "../components/context/AuthContext";
import { useSubmitNewTraining } from "../api/mutations";
import { formatTrainingData } from "../utils/transformTrainingData";
import { trainerDataRequest, userInfoRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import MetadataContext from "../components/context/MetadataContext";


interface StepData {
    [key: string]: any;
}

const UploadTrainingPage = () => {

    const authData = useContext(AuthContext)
    const submitTrainingDataMutation = useSubmitNewTraining(authData.access_token)
    const navigate = useNavigate();

    const { data: meData, isLoading: isMeLoading } = useQuery({
        queryKey: ['me'],
        queryFn: () => userInfoRequest(authData.access_token),
        enabled: authData.access_token !== ""
    })

    const [step, setStep] = useState<"welcome" | "metadata" | "editor" | "end">("welcome");
    const [createdTrainingId, setCreatedTrainingId] = useState<string | null>(null);

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

    useEffect(() => {
        if (meData?.username) {
            setSavedData(prev => ({
                ...prev,
                trainer_name: meData.username
            }));
        }
    }, [meData]);

    const { data: trainerData = [], isLoading: isTrainerLoading, status: trainerStatus } = useQuery<any, Error>({
        queryKey: ['trainerData'],
        queryFn: () => trainerDataRequest(authData.access_token)
    })

    const { data: userData = [], isLoading: isUserLoading, status: userStatus } = useQuery<any, Error>({
        queryKey: ['userData'],
        queryFn: () => userInfoRequest(authData.access_token)
    })

    const handleSubmit = () => {
        console.log("Saved data: ", savedData);
        const formattedData = formatTrainingData(savedData, trainerData, userData);

        submitTrainingDataMutation.mutate(formattedData, {
            onSuccess: (data) => {
                console.log("Received data from server:", data);
                const newTrainingId = data.id;
                setCreatedTrainingId(newTrainingId);
                setStep("end");
            },
            onError: (error) => {
                console.error("Error:", error);
            }
        });
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
        <div className="training-page basic-page">

            <div style={{ position: "relative" }}>
                <svg
                    width="1200"
                    height="1200"
                    viewBox="0 0 1200 1200"
                    style={{
                        position: "absolute",
                        top: "-400px",
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

            <div>
                {step === "welcome" && (
                    <div className="centered-content">

                        <div className="step-title-main">Welcome to the Training Course Creator</div>
                        <p>Let's help you design a personalized fitness program from scratch.</p>
                        <div className="button-group-welcome">
                            <button className="btn-basic-black" onClick={nextStep}>Get Started</button>
                        </div>
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
                            <button onClick={() => navigate(`/course/${createdTrainingId}`)} className="btn-basic-black">
                                View plan
                            </button>
                            <button onClick={() => navigate('/')} className="btn-basic-white">
                                Main menu
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadTrainingPage;