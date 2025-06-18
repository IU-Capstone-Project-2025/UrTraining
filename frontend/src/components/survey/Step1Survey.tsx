import React from 'react'
import type { TrainingProfileUpdate } from '../../utils/auth'

interface Step1SurveyProps {
    formData: TrainingProfileUpdate;
    updateFormData: (updates: Partial<TrainingProfileUpdate>) => void;
}

const Step1Survey: React.FC<Step1SurveyProps> = ({ formData, updateFormData }) => {
    const handleChange = (field: keyof TrainingProfileUpdate, value: any) => {
        updateFormData({ [field]: value });
    };

    return (
        <>
            <div className="survey__title">
                <h2>Basic Information</h2>
            </div>
            
            <div className="survey__options__section">
                <p>What is your gender?</p>
                <div className="survey__section__forms">
                    <form>
                        <label className="radio-basic-black">
                            <input
                                type="radio"
                                name="gender"
                                value="male"
                                checked={formData.gender === 'male'}
                                onChange={(e) => handleChange('gender', e.target.value)}
                            />
                            <div>Male</div>
                        </label>
                        <label className="radio-basic-black">
                            <input
                                type="radio"
                                name="gender"
                                value="female"
                                checked={formData.gender === 'female'}
                                onChange={(e) => handleChange('gender', e.target.value)}
                            />
                            <div>Female</div>
                        </label>
                    </form>
                </div>
            </div>

            <div className="survey__options__section">
                <p>Personal Details</p>
                <div className="survey__section__forms">
                    <form>
                        <input
                            type="number"
                            name="age"
                            className="form-basic-white"
                            placeholder="Age (13-100)"
                            value={formData.age || ''}
                            onChange={(e) => handleChange('age', e.target.value ? parseInt(e.target.value) : undefined)}
                            min="13"
                            max="100"
                        />
                        <input
                            type="number"
                            name="height_cm"
                            className="form-basic-white"
                            placeholder="Height (cm)"
                            value={formData.height_cm || ''}
                            onChange={(e) => handleChange('height_cm', e.target.value ? parseInt(e.target.value) : undefined)}
                            min="100"
                            max="250"
                        />
                        <input
                            type="number"
                            name="weight_kg"
                            className="form-basic-white"
                            placeholder="Weight (kg)"
                            step="0.1"
                            value={formData.weight_kg || ''}
                            onChange={(e) => handleChange('weight_kg', e.target.value ? parseFloat(e.target.value) : undefined)}
                            min="30"
                            max="300"
                        />
                    </form>
                </div>
            </div>
        </>
    )
}

export default Step1Survey