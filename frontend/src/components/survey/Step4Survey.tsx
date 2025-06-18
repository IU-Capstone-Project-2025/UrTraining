import React from 'react'
import type { TrainingProfileUpdate } from '../../utils/auth'

interface Step4SurveyProps {
    formData: TrainingProfileUpdate;
    updateFormData: (updates: Partial<TrainingProfileUpdate>) => void;
}

const Step4Survey: React.FC<Step4SurveyProps> = ({ formData, updateFormData }) => {
    const trainingTypes = [
        {
            key: 'strength_training' as keyof TrainingProfileUpdate,
            label: 'Strength Training',
            description: 'Weight lifting, resistance exercises, bodyweight training'
        },
        {
            key: 'cardio' as keyof TrainingProfileUpdate,
            label: 'Cardio',
            description: 'Running, cycling, swimming, aerobic exercises'
        },
        {
            key: 'hiit' as keyof TrainingProfileUpdate,
            label: 'HIIT (High-Intensity Interval Training)',
            description: 'Short bursts of intense exercise with rest periods'
        },
        {
            key: 'yoga_pilates' as keyof TrainingProfileUpdate,
            label: 'Yoga/Pilates',
            description: 'Flexibility, balance, mindfulness, core strengthening'
        },
        {
            key: 'functional_training' as keyof TrainingProfileUpdate,
            label: 'Functional Training',
            description: 'Movement patterns for daily activities, crossfit, kettlebells'
        },
        {
            key: 'stretching' as keyof TrainingProfileUpdate,
            label: 'Stretching/Mobility',
            description: 'Flexibility work, recovery, injury prevention'
        }
    ];

    const handleRatingChange = (trainingType: keyof TrainingProfileUpdate, rating: number) => {
        updateFormData({ [trainingType]: rating });
    };

    const RatingScale: React.FC<{ 
        trainingType: keyof TrainingProfileUpdate; 
        label: string; 
        description: string; 
        currentValue?: number 
    }> = ({ trainingType, label, description, currentValue }) => {
        return (
            <div className="survey__options__section" style={{ marginBottom: '25px' }}>
                <div style={{ marginBottom: '10px' }}>
                    <strong>{label}</strong>
                    <p style={{ fontSize: '14px', color: '#666', margin: '5px 0' }}>{description}</p>
                </div>
                <div className="survey__section__forms">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <span style={{ fontSize: '14px', minWidth: '80px' }}>Not interested</span>
                        {[1, 2, 3, 4, 5].map(rating => (
                            <label key={rating} className="radio-basic-black" style={{ margin: 0 }}>
                                <input
                                    type="radio"
                                    name={`${trainingType}_rating`}
                                    value={rating}
                                    checked={currentValue === rating}
                                    onChange={() => handleRatingChange(trainingType, rating)}
                                />
                                <div>{rating}</div>
                            </label>
                        ))}
                        <span style={{ fontSize: '14px', minWidth: '80px' }}>Very interested</span>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <>
            <div className="survey__title">
                <h2>Training Interests</h2>
            </div>
            
            <div style={{ marginBottom: '20px' }}>
                <p>Rate your interest in each type of training on a scale of 1-5:</p>
                <p style={{ fontSize: '14px', color: '#666' }}>
                    1 = Not interested at all, 5 = Very interested
                </p>
            </div>

            {trainingTypes.map(type => (
                <RatingScale
                    key={type.key}
                    trainingType={type.key}
                    label={type.label}
                    description={type.description}
                    currentValue={formData[type.key] as number}
                />
            ))}
        </>
    )
}

export default Step4Survey 