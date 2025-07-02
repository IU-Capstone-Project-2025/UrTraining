import React, { useState } from "react";
import TrainingEditor from "../components/CourseEditor";
import Metadata from "../components/Metadata";

interface StepData {
    [key: string]: any;
}

const UploadTrainingPage = () => {

    const [savedData, setSavedData] = useState({
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

    const handleSave = () => {
        console.log("Saved data:");
        // Можно передать savedData в TrainingEditor здесь
    };

    return (
        <div>
        <Metadata savedData={savedData} setSavedData={setSavedData} />
        <button onClick={handleSave} className="btn-basic-black">
            Continue
        </button>

        {/* Пример передачи данных в другой компонент */}
        <TrainingEditor savedData={savedData} setSavedData={setSavedData} />
        </div>
    );
};

export default UploadTrainingPage;