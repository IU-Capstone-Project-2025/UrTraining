import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import "../css/Survey.css"
import Step1Survey from './survey/Step1Survey';
import Step2Survey from './survey/Step2Survey';
import Step3Survey from './survey/Step3Survey';
import Step4Survey from './survey/Step4Survey';
import { authAPI } from '../utils/auth';
import type { TrainingProfileUpdate } from '../utils/auth';

const Survey = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();
    const step = parseInt(searchParams.get('step') || '') || 1;

    const [formData, setFormData] = useState<TrainingProfileUpdate>({
        // Basic Information
        gender: '',
        age: undefined,
        height_cm: undefined,
        weight_kg: undefined,
        
        // Training Goals
        training_goals: [],
        
        // Training Experience
        training_level: '',
        frequency_last_3_months: '',
        
        // Preferences
        training_location: '',
        location_details: '',
        session_duration: '',
        
        // Health
        joint_back_problems: undefined,
        chronic_conditions: undefined,
        health_details: '',
        
        // Training Types (1-5 scale)
        strength_training: undefined,
        cardio: undefined,
        hiit: undefined,
        yoga_pilates: undefined,
        functional_training: undefined,
        stretching: undefined,
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        if (step < 1 || step > 4) {
            goToStep(1);
        }
    }, [step]);

    useEffect(() => {
        // Load existing profile data when component mounts
        loadExistingProfile();
    }, []);

    const loadExistingProfile = async () => {
        try {
            const profileData = await authAPI.getTrainingProfile();
            const profile = profileData.training_profile;
            
            if (profile) {
                setFormData({
                    // Basic Information
                    gender: profile.basic_information?.gender || '',
                    age: profile.basic_information?.age,
                    height_cm: profile.basic_information?.height_cm,
                    weight_kg: profile.basic_information?.weight_kg,
                    
                    // Training Goals
                    training_goals: profile.training_goals || [],
                    
                    // Training Experience
                    training_level: profile.training_experience?.level || '',
                    frequency_last_3_months: profile.training_experience?.frequency_last_3_months || '',
                    
                    // Preferences
                    training_location: profile.preferences?.training_location || '',
                    location_details: profile.preferences?.location_details || '',
                    session_duration: profile.preferences?.session_duration || '',
                    
                    // Health
                    joint_back_problems: profile.health?.joint_back_problems,
                    chronic_conditions: profile.health?.chronic_conditions,
                    health_details: profile.health?.health_details || '',
                    
                    // Training Types
                    strength_training: profile.training_types?.strength_training,
                    cardio: profile.training_types?.cardio,
                    hiit: profile.training_types?.hiit,
                    yoga_pilates: profile.training_types?.yoga_pilates,
                    functional_training: profile.training_types?.functional_training,
                    stretching: profile.training_types?.stretching,
                });
            }
        } catch (error) {
            console.error('Error loading profile:', error);
            // Continue with empty form if profile doesn't exist
        }
    };

    const goToStep = (newStep: number) => {
        setSearchParams({ step: newStep.toString() });
        setError('');
        setSuccess('');
    };

    const updateFormData = (updates: Partial<TrainingProfileUpdate>) => {
        setFormData(prev => ({ ...prev, ...updates }));
    };

    const handleNext = () => {
        if (step < 4) {
            goToStep(step + 1);
        }
    };

    const handleBack = () => {
        if (step > 1) {
            goToStep(step - 1);
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError('');
        setSuccess('');
        
        try {
            // Clean up the data before sending
            const cleanedData: TrainingProfileUpdate = {};
            
            // Only include non-empty values
            if (formData.gender) cleanedData.gender = formData.gender;
            if (formData.age) cleanedData.age = formData.age;
            if (formData.height_cm) cleanedData.height_cm = formData.height_cm;
            if (formData.weight_kg) cleanedData.weight_kg = formData.weight_kg;
            
            if (formData.training_goals && formData.training_goals.length > 0) {
                cleanedData.training_goals = formData.training_goals;
            }
            
            if (formData.training_level) cleanedData.training_level = formData.training_level;
            if (formData.frequency_last_3_months) cleanedData.frequency_last_3_months = formData.frequency_last_3_months;
            
            if (formData.training_location) cleanedData.training_location = formData.training_location;
            if (formData.location_details) cleanedData.location_details = formData.location_details;
            if (formData.session_duration) cleanedData.session_duration = formData.session_duration;
            
            if (formData.joint_back_problems !== undefined) cleanedData.joint_back_problems = formData.joint_back_problems;
            if (formData.chronic_conditions !== undefined) cleanedData.chronic_conditions = formData.chronic_conditions;
            if (formData.health_details) cleanedData.health_details = formData.health_details;
            
            if (formData.strength_training) cleanedData.strength_training = formData.strength_training;
            if (formData.cardio) cleanedData.cardio = formData.cardio;
            if (formData.hiit) cleanedData.hiit = formData.hiit;
            if (formData.yoga_pilates) cleanedData.yoga_pilates = formData.yoga_pilates;
            if (formData.functional_training) cleanedData.functional_training = formData.functional_training;
            if (formData.stretching) cleanedData.stretching = formData.stretching;

            await authAPI.updateTrainingProfile(cleanedData);
            
            setSuccess('Training profile updated successfully!');
            
            // Navigate to appropriate page after successful submission
            setTimeout(() => {
                navigate('/trainee-begin');
            }, 2000);
            
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to update profile. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const getStepInfo = () => {
        switch (step) {
            case 1:
                return {
                    title: "Basic Information",
                    description: "Tell us about yourself so we can create the perfect training plan for you."
                };
            case 2:
                return {
                    title: "Training Goals & Experience",
                    description: "What do you want to achieve and what's your training background?"
                };
            case 3:
                return {
                    title: "Preferences & Health",
                    description: "Where do you like to train and any health considerations?"
                };
            case 4:
                return {
                    title: "Training Interests",
                    description: "Rate your interest in different types of training (1-5 scale)."
                };
            default:
                return { title: "", description: "" };
        }
    };

    const currentStepInfo = getStepInfo();

    return (
        <div className="survey basic-page">
            <div className="survey__navbar">
                {[1, 2, 3, 4].map((s) => (
                    <h3 
                        key={s}
                        className={step === s ? "survey__navbar__selected" : ""}
                        onClick={() => goToStep(s)}
                        style={{ cursor: 'pointer' }}
                    >
                        Step {s}
                    </h3>
                ))}
            </div>
            <div className="survey__container">
                <div className="survey__options">
                    {step === 1 && <Step1Survey formData={formData} updateFormData={updateFormData} />}
                    {step === 2 && <Step2Survey formData={formData} updateFormData={updateFormData} />}
                    {step === 3 && <Step3Survey formData={formData} updateFormData={updateFormData} />}
                    {step === 4 && <Step4Survey formData={formData} updateFormData={updateFormData} />}
                </div>
                <div className="survey__info">
                    <div className="survey__info__description">
                        <div className="survey__title">
                            <h2>{currentStepInfo.title}</h2>
                        </div>
                        <p>{currentStepInfo.description}</p>
                        
                        {error && (
                            <div style={{ 
                                color: 'red', 
                                backgroundColor: '#ffebee', 
                                padding: '10px', 
                                borderRadius: '4px', 
                                marginTop: '15px',
                                border: '1px solid #ffcdd2'
                            }}>
                                {error}
                            </div>
                        )}
                        
                        {success && (
                            <div style={{ 
                                color: 'green', 
                                backgroundColor: '#e8f5e8', 
                                padding: '10px', 
                                borderRadius: '4px', 
                                marginTop: '15px',
                                border: '1px solid #c8e6c9'
                            }}>
                                {success}
                            </div>
                        )}
                    </div>
                    <div className="survey__info__button">
                        {step !== 1 && (
                            <button 
                                className="btn-basic-white" 
                                onClick={handleBack}
                                disabled={loading}
                            >
                                Back
                            </button>
                        )}
                        {step !== 4 && (
                            <button 
                                className="btn-basic-black" 
                                onClick={handleNext}
                                disabled={loading}
                            >
                                Continue
                            </button>
                        )}
                        {step === 4 && (
                            <button 
                                className="btn-basic-black"
                                onClick={handleSubmit}
                                disabled={loading}
                            >
                                {loading ? 'Saving...' : 'Complete Profile'}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Survey