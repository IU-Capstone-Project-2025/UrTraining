import React from 'react'
import type { TrainingProfileUpdate } from '../../utils/auth'

interface Step2SurveyProps {
    formData: TrainingProfileUpdate;
    updateFormData: (updates: Partial<TrainingProfileUpdate>) => void;
}

const Step2Survey: React.FC<Step2SurveyProps> = ({ formData, updateFormData }) => {
    const trainingGoalsOptions = [
        'weight_loss',
        'muscle_gain',
        'improve_flexibility',
        'increase_strength',
        'improve_endurance',
        'maintain_fitness',
        'rehabilitation',
        'stress_relief'
    ];

    const trainingLevels = [
        { value: 'beginner', label: 'Beginner (0-6 months)' },
        { value: 'intermediate', label: 'Intermediate (6 months - 2 years)' },
        { value: 'advanced', label: 'Advanced (2+ years)' },
        { value: 'expert', label: 'Expert/Professional' }
    ];

    const frequencyOptions = [
        { value: 'never', label: 'Never' },
        { value: '1_2_times_week', label: '1-2 times per week' },
        { value: '3_4_times_week', label: '3-4 times per week' },
        { value: '5_6_times_week', label: '5-6 times per week' },
        { value: 'daily', label: 'Daily' }
    ];

    const handleGoalChange = (goal: string, checked: boolean) => {
        const currentGoals = formData.training_goals || [];
        let newGoals;
        
        if (checked) {
            newGoals = [...currentGoals, goal];
        } else {
            newGoals = currentGoals.filter(g => g !== goal);
        }
        
        updateFormData({ training_goals: newGoals });
    };

    return (
        <>
            <div className="survey__title">
                <h2>Training Goals & Experience</h2>
            </div>
            
            <div className="survey__options__section">
                <p>What are your training goals? (Select all that apply)</p>
                <div className="survey__section__forms">
                    <form>
                        {trainingGoalsOptions.map(goal => (
                            <label key={goal} className="checkbox-basic-white" style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                                <input
                                    type="checkbox"
                                    checked={formData.training_goals?.includes(goal) || false}
                                    onChange={(e) => handleGoalChange(goal, e.target.checked)}
                                />
                                <span style={{ marginLeft: '8px', textTransform: 'capitalize' }}>
                                    {goal.replace(/_/g, ' ')}
                                </span>
                            </label>
                        ))}
                    </form>
                </div>
            </div>

            <div className="survey__options__section">
                <p>What is your training experience level?</p>
                <div className="survey__section__forms">
                    <form>
                        {trainingLevels.map(level => (
                            <label key={level.value} className="radio-basic-black">
                                <input
                                    type="radio"
                                    name="training_level"
                                    value={level.value}
                                    checked={formData.training_level === level.value}
                                    onChange={(e) => updateFormData({ training_level: e.target.value })}
                                />
                                <div>{level.label}</div>
                            </label>
                        ))}
                    </form>
                </div>
            </div>

            <div className="survey__options__section">
                <p>How often have you been training in the last 3 months?</p>
                <div className="survey__section__forms">
                    <form>
                        {frequencyOptions.map(freq => (
                            <label key={freq.value} className="radio-basic-black">
                                <input
                                    type="radio"
                                    name="frequency_last_3_months"
                                    value={freq.value}
                                    checked={formData.frequency_last_3_months === freq.value}
                                    onChange={(e) => updateFormData({ frequency_last_3_months: e.target.value })}
                                />
                                <div>{freq.label}</div>
                            </label>
                        ))}
                    </form>
                </div>
            </div>
        </>
    )
}

export default Step2Survey 