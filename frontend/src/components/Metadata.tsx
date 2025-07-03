import React, { useState } from 'react'
import '../css/Course.css';

interface StepData {
    [key: string]: any;
}

interface MetadataProps {
  savedData: StepData;
  setSavedData: React.Dispatch<React.SetStateAction<StepData>>;
  onNext: () => void;
  onBack: () => void;
}

const Metadata: React.FC<MetadataProps> = ({ savedData, setSavedData, onBack, onNext }) => {
    const [goals, setGoals] = useState(1)
    const [environment, setEnvironment] = useState(1)
    const [age, setAge] = useState(1)
    const [limitations, setLimitations] = useState(1)
    const [equipment, setEquipment] = useState(1)
    const [content, setContent] = useState(1)
    const [feedback, setFeedback] = useState(1)
    const [tags, setTags] = useState(1)

    type MetadataFieldType = 'text' | 'number' | 'Array';
    type MetadataKey =
        | 'activity_type'
        | 'program_goal'
        | 'training_environment'
        | 'difficulty_level'
        | 'course_duration'
        | 'weekly_training_frequency'
        | 'average_workout_duration'
        | 'age_group'
        | 'gender_orientation'
        | 'physical_limitations'
        | 'required_equipment'
        | 'tags'
        | 'course_title'
        | 'program_description';

    const metadataDefault: Record<MetadataKey, MetadataFieldType> = {
        activity_type: "text",
        program_goal: "Array",
        training_environment: "Array",
        difficulty_level: "text",
        course_duration: "number",
        weekly_training_frequency: "text",
        average_workout_duration: "text",
        age_group: "Array",
        gender_orientation: "text",
        physical_limitations: "Array",
        required_equipment: "Array",
        tags: "Array",
        course_title: "text",
        program_description: "text",
    }

    const metadataState = {
        program_goal: {
            value: goals,
            setFunction: setGoals
        },
        training_environment: {
            value: environment,
            setFunction: setEnvironment
        },
        age_group: {
            value: age,
            setFunction: setAge
        },
        physical_limitations: {
            value: limitations,
            setFunction: setLimitations
        },
        required_equipment: {
            value: equipment,
            setFunction: setEquipment
        },
        tags: {
            value: tags,
            setFunction: setTags
        }
    }

    const metadataNames = {
        activity_type: "Activity Type",
        program_goal: "Program Goal",
        training_environment: "Training Environment",
        difficulty_level: "Difficulty Level",
        course_duration: "Course Duration",
        weekly_training_frequency: "Weekly Training Frequency",
        average_workout_duration: "Average Workout Duration",
        age_group: "Age Group",
        gender_orientation: "Gender Orientation",
        physical_limitations: "Physical Limitations",
        required_equipment: "Required Equipment",
        tags: "Tags",
        course_title: "Course Title",
        program_description: "Program Description",
    }

    const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
        const target = event.target as HTMLInputElement;
        const name = target.name as MetadataKey;
        const value = target.value;

        if (metadataDefault[name] === "Array") {
            const form = target.form;
            if (!form) return;

            const inputs = Array.from(form.elements).filter(
                (el): el is HTMLInputElement => el instanceof HTMLInputElement && el.name === name
            );

            const values = inputs.map(input => input.value);

            setSavedData(prev => ({
                ...prev,
                [name]: values
            }));
        } else {
            // Regular text or number input
            setSavedData(prev => ({
                ...prev,
                [name]: value
            }));
        }

        console.log(savedData);

    };

    const metadataKeys = Object.keys(metadataDefault) as MetadataKey[]

    return (
        <div className="course__container">
            <h2 className="step-title">Step 1: Course Metadata</h2>
            <div className='course__structure__metadata'>
                <div className='course__metadata__fields'>
                    {metadataKeys.map((key, index) => {
                        return (
                            <div className='course__metadata__field' key={index}>
                                <p className='course__field__name'>{metadataNames[key]}</p>
                                {(metadataDefault[key] === "text" ||
                                    metadataDefault[key] === "number") &&
                                    <form
                                        className='course__field__form'
                                        onChange={handleChange}>
                                        <input
                                            className='course__field__input'
                                            type={metadataDefault[key]}
                                            name={key}
                                        />
                                    </form>
                                }

                                {metadataDefault[key] === "Array" && (key in metadataState) && (() => {
                                    // Now TS knows key is one of metadataState's keys
                                    const stateKey = key as keyof typeof metadataState;
                                    const { value, setFunction } = metadataState[stateKey];

                                    return (
                                        <div className="course__input__array">
                                            <form className="course__field__form" onChange={handleChange}>
                                                {Array.from({ length: value }).map((_, i) => (
                                                    <input
                                                        key={i}
                                                        className="course__field__input"
                                                        type="text"
                                                        name={key}
                                                    />
                                                ))}
                                            </form>
                                            <button
                                                className="btn-basic-white course__array__button"
                                                onClick={() => setFunction(value + 1)}
                                            >
                                                Add option
                                            </button>
                                        </div>
                                    );
                                })()}
                            </div>
                        )
                    })}
                </div>
            </div>
            <div className="button-row">
                <button className="btn-basic-black" onClick={onBack}>Back</button>
                <button className="btn-basic-black" onClick={onNext}>Continue</button>
            </div>
        </div>
    )
}

export default Metadata