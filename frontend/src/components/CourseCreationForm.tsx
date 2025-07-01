import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface TrainingMetadata {
  courseTitle: string;
  activityType: string;
  programGoal: string[];
  trainingEnvironment: string[];
  difficultyLevel: string;
  courseDurationWeeks: number;
  weeklyTrainingFrequency: string;
  averageWorkoutDuration: string;
  ageGroup: string[];
  genderOrientation: string;
  physicalLimitations: string[];
  requiredEquipment: string[];
  courseLanguage: string;
  visualContent: string[];
  trainerFeedbackOptions: string[];
  tags: string[];
}

const CourseCreationForm = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState<number>(1);
  const [formData, setFormData] = useState<TrainingMetadata>({
    courseTitle: '',
    activityType: '',
    programGoal: [],
    trainingEnvironment: [],
    difficultyLevel: '',
    courseDurationWeeks: 4,
    weeklyTrainingFrequency: '',
    averageWorkoutDuration: '',
    ageGroup: [],
    genderOrientation: '',
    physicalLimitations: [],
    requiredEquipment: [],
    courseLanguage: '',
    visualContent: [],
    trainerFeedbackOptions: [],
    tags: []
  });

  const options = {
    activityType: ['Bodybuilding', 'Cardio', 'HIIT', 'Yoga', 'Pilates', 'Functional Training'],
    programGoal: ['Weight Loss', 'Muscle Gain', 'Endurance Improvement', 'Flexibility', 'Rehabilitation'],
    difficultyLevel: ['Beginner', 'Intermediate', 'Advanced'],
    // ... другие варианты
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleMultiSelect = (name: keyof TrainingMetadata, value: string) => {
    setFormData(prev => {
      const currentValues = prev[name] as string[];
      return {
        ...prev,
        [name]: currentValues.includes(value)
          ? currentValues.filter(v => v !== value)
          : [...currentValues, value]
      };
    });
  };

  const nextStep = () => setStep(prev => prev + 1);
  const prevStep = () => setStep(prev => prev - 1);

  const handleSubmit = () => {
    navigate('/course-editor', { state: { metadata: formData } });
  };

  return (
    <div className="training-creation-form">
      <h1>New training plan creation</h1>
      
      <div className="progress-bar">
        {[1, 2, 3].map((i) => (
          <div 
            key={i} 
            className={`progress-step ${i <= step ? 'active' : ''}`}
          >
            Шаг {i}
          </div>
        ))}
      </div>

      {/* Шаг 1: Основная информация */}
      {step === 1 && (
        <div className="form-step">
          <div className="form-group">
            <label>Course title</label>
            <input
              type="text"
              name="courseTitle"
              value={formData.courseTitle}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Activity type*</label>
            <select
              name="activityType"
              value={formData.activityType}
              onChange={handleChange}
              required
            >
              <option value="">Choose the option</option>
              {options.activityType.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Purposes of program*</label>
            <div className="checkbox-group">
              {options.programGoal.map(goal => (
                <label key={goal}>
                  <input
                    type="checkbox"
                    checked={formData.programGoal.includes(goal)}
                    onChange={() => handleMultiSelect('programGoal', goal)}
                  />
                  {goal}
                </label>
              ))}
            </div>
          </div>

          <button onClick={nextStep}>Далее</button>
        </div>
      )}

      {step === 2 && (
        <div className="form-step">
          <div className="form-group">
            <label>Difficulty level*</label>
            <select
              name="difficultyLevel"
              value={formData.difficultyLevel}
              onChange={handleChange}
              required
            >
              <option value="">Choose the level:</option>
              {options.difficultyLevel.map(level => (
                <option key={level} value={level}>{level}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Course duration in weeks*</label>
            <input
              type="number"
              name="courseDurationWeeks"
              min="1"
              max="52"
              value={formData.courseDurationWeeks}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Trainings per week*</label>
            <input
              type="text"
              name="weeklyTrainingFrequency"
              value={formData.weeklyTrainingFrequency}
              onChange={handleChange}
              placeholder="Например: 3-4 раза"
              required
            />
          </div>

          <div className="form-buttons">
            <button onClick={prevStep}>Назад</button>
            <button onClick={nextStep}>Далее</button>
          </div>
        </div>
      )}

      {/* Шаг 3: Дополнительные параметры */}
      {step === 3 && (
        <div className="form-step">
          <div className="form-group">
            <label>Equipment:</label>
            <input
              type="text"
              name="requiredEquipment"
              value={formData.requiredEquipment.join(', ')}
              onChange={(e) => setFormData(prev => ({
                ...prev,
                requiredEquipment: e.target.value.split(',').map(item => item.trim())
              }))}
              placeholder="Укажите через запятую"
            />
          </div>

          <div className="form-group">
            <label>Теги</label>
            <input
              type="text"
              name="tags"
              value={formData.tags.join(', ')}
              onChange={(e) => setFormData(prev => ({
                ...prev,
                tags: e.target.value.split(',').map(item => item.trim())
              }))}
              placeholder="Укажите через запятую"
            />
          </div>

          <div className="form-buttons">
            <button onClick={prevStep}>Back</button>
            <button onClick={handleSubmit}>Create trainings</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseCreationForm;