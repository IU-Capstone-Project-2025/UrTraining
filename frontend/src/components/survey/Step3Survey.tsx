import React from 'react'
import type { TrainingProfileUpdate } from '../../utils/auth'

interface Step3SurveyProps {
    formData: TrainingProfileUpdate;
    updateFormData: (updates: Partial<TrainingProfileUpdate>) => void;
}

const Step3Survey: React.FC<Step3SurveyProps> = ({ formData, updateFormData }) => {
    const trainingLocations = [
        { value: 'gym', label: 'Gym' },
        { value: 'home', label: 'Home' },
        { value: 'outdoor', label: 'Outdoor' },
        { value: 'studio', label: 'Studio/Class' }
    ];

    const locationDetails = [
        { value: 'full_fitness_center', label: 'Full fitness center' },
        { value: 'basic_gym', label: 'Basic gym equipment' },
        { value: 'no_equipment', label: 'No equipment available' },
        { value: 'limited_equipment', label: 'Limited equipment' },
        { value: 'full_home_gym', label: 'Full home gym setup' }
    ];

    const sessionDurations = [
        { value: '15_30_min', label: '15-30 minutes' },
        { value: '30_45_min', label: '30-45 minutes' },
        { value: '45_60_min', label: '45-60 minutes' },
        { value: '60_90_min', label: '60-90 minutes' },
        { value: '90_plus_min', label: '90+ minutes' }
    ];

    return (
        <>
            <div className="survey__title">
                <h2>Preferences & Health</h2>
            </div>
            
            <div className="survey__options__section">
                <p>Where do you prefer to train?</p>
                <div className="survey__section__forms">
                    <form>
                        {trainingLocations.map(location => (
                            <label key={location.value} className="radio-basic-black">
                                <input
                                    type="radio"
                                    name="training_location"
                                    value={location.value}
                                    checked={formData.training_location === location.value}
                                    onChange={(e) => updateFormData({ training_location: e.target.value })}
                                />
                                <div>{location.label}</div>
                            </label>
                        ))}
                    </form>
                </div>
            </div>

            <div className="survey__options__section">
                <p>What equipment/facilities do you have access to?</p>
                <div className="survey__section__forms">
                    <form>
                        {locationDetails.map(detail => (
                            <label key={detail.value} className="radio-basic-black">
                                <input
                                    type="radio"
                                    name="location_details"
                                    value={detail.value}
                                    checked={formData.location_details === detail.value}
                                    onChange={(e) => updateFormData({ location_details: e.target.value })}
                                />
                                <div>{detail.label}</div>
                            </label>
                        ))}
                    </form>
                </div>
            </div>

            <div className="survey__options__section">
                <p>How long do you prefer your training sessions?</p>
                <div className="survey__section__forms">
                    <form>
                        {sessionDurations.map(duration => (
                            <label key={duration.value} className="radio-basic-black">
                                <input
                                    type="radio"
                                    name="session_duration"
                                    value={duration.value}
                                    checked={formData.session_duration === duration.value}
                                    onChange={(e) => updateFormData({ session_duration: e.target.value })}
                                />
                                <div>{duration.label}</div>
                            </label>
                        ))}
                    </form>
                </div>
            </div>

            <div className="survey__options__section">
                <p>Health Considerations</p>
                <div className="survey__section__forms">
                    <form>
                        <label className="checkbox-basic-white" style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                            <input
                                type="checkbox"
                                checked={formData.joint_back_problems === true}
                                onChange={(e) => updateFormData({ joint_back_problems: e.target.checked })}
                            />
                            <span style={{ marginLeft: '8px' }}>
                                I have joint or back problems
                            </span>
                        </label>
                        
                        <label className="checkbox-basic-white" style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                            <input
                                type="checkbox"
                                checked={formData.chronic_conditions === true}
                                onChange={(e) => updateFormData({ chronic_conditions: e.target.checked })}
                            />
                            <span style={{ marginLeft: '8px' }}>
                                I have chronic health conditions
                            </span>
                        </label>
                        
                        <textarea
                            name="health_details"
                            className="form-basic-white"
                            placeholder="Please describe any health conditions, injuries, or limitations we should know about (optional)"
                            value={formData.health_details || ''}
                            onChange={(e) => updateFormData({ health_details: e.target.value })}
                            rows={4}
                            style={{ width: '100%', resize: 'vertical', marginTop: '10px' }}
                        />
                    </form>
                </div>
            </div>
        </>
    )
}

export default Step3Survey 