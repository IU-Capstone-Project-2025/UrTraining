import React, { useContext, useState } from 'react'
import '../css/Course.css'
import MetadataContext from './context/MetadataContext'

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
  const metadataContext = useContext(MetadataContext)

  const [arrayCounts, setArrayCounts] = useState<Record<string, number>>({
    program_goal: 1,
    training_environment: 1,
    age_group: 1,
    physical_limitations: 1,
    required_equipment: 1,
    tags: 1
  });

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
    | 'tags';

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
    tags: "Array"
  };

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
    tags: "Tags"
  };

  const metadataOptions: Record<MetadataKey, string[]> = {
    activity_type: ["Strength Training", "Cardio", "HIIT", "Yoga", "Pilates", "Functional Training", "CrossFit", "Bodybuilding", "Stretching", "Running", "Swimming", "Cycling", "Boxing/Martial Arts", "Dancing"],
    program_goal: ["Weight Loss", "Muscle Gain", "Endurance Improvement", "Flexibility Improvement", "Maintaining Fitness", "Competition Preparation", "Rehabilitation", "Stress Relief", "Health Improvement"],
    training_environment: ["Home Without Equipment", "Home With Basic Equipment", "Gym", "Outdoors", "Pool", "Universal"],
    difficulty_level: ["Beginner", "Intermediate", "Advanced", "All Levels (Adaptive Program)"],
    course_duration: ["1", "2", "5"],
    weekly_training_frequency: ["1-2 times", "3-4 times", "5-6 times"],
    average_workout_duration: ["Up to 30 minutes", "30-45 minutes", "45-60 minutes", "More than 60 minutes"],
    age_group: ["Teens (13-17)", "Young Adults (18-30)", "Adults (31-50)", "Seniors (51+)", "All Ages"],
    gender_orientation: ["For Women", "For Men", "Unisex"],
    physical_limitations: ["Joint Issues", "Back Problems", "Post-Injury Recovery", "Pregnancy/Postpartum", "Limited Mobility", "Cardiovascular Diseases", "Diabetes", "Overweight", "Not Adapted (Healthy Only)"],
    required_equipment: ["No Equipment", "Fitness Mat", "Dumbbells", "Barbell and Plates", "Gym Machines", "Pull-up/Dip Bars", "Resistance Bands", "Jump Rope", "Fitball", "TRX/Suspension Trainer", "Step Platform", "Boxing Bag", "Specific Equipment (specify)"],
    tags: ["Weight Loss", "Muscle Gain", "Strength", "Endurance", "Flexibility", "Balance", "Coordination", "Speed", "Rehabilitation", "Posture", "Abs", "Glutes", "Arms", "Legs", "Back", "Explosive Strength", "Mobility", "Beach Body", "High Intensity", "Low Intensity", "No Jumps", "Knee Safe", "Short Workouts", "Morning Workouts", "Recovery", "For Beginners", "For Experienced", "No Equipment", "Minimal Equipment", "Marathon Prep", "Functionality", "Injury Prevention", "Sports Performance", "Home Workouts", "Fat Burning", "Active Longevity", "Anti-Stress", "Energy", "Better Sleep", "Metabolism"]
  };

  const handleSelectChange = (name: MetadataKey, value: string, index?: number) => {
    setSavedData(prev => {
      if (metadataDefault[name] === "Array") {
        const existing = Array.isArray(prev[name]) ? [...prev[name]] : [];
        existing[index ?? 0] = value;
        return { ...prev, [name]: existing };
      } else {
        return { ...prev, [name]: value };
      }
    });
  };

  const handleAddOption = (key: string) => {
    setArrayCounts(prev => ({
      ...prev,
      [key]: (prev[key] || 1) + 1
    }));
  };

  const metadataKeys = Object.keys(metadataDefault) as MetadataKey[];

  return (
    <div className="course__container">
      <h2 className="step-title">Step 1: Course Metadata</h2>
      <div className='course__structure__metadata'>
        <div className='course__metadata__fields'>
          {metadataKeys.map((key) => (
            <div className='course__metadata__field' key={key}>
              <p className='course__field__name'>{metadataNames[key]}</p>

              {metadataDefault[key] === "Array" && (
                <div className="course__input__array">
                  {Array.from({ length: arrayCounts[key] || 1 }).map((_, i) => (
                    <select
                      key={i}
                      className="course__field__input"
                      name={key}
                      value={savedData[key]?.[i] || ""}
                      onChange={e => handleSelectChange(key, e.target.value, i)}
                    >
                      <option value="" disabled>Select an option</option>
                      {metadataOptions[key].map((option, idx) => (
                        <option key={idx} value={option}>{option}</option>
                      ))}
                    </select>
                  ))}
                  <button
                    className="btn-basic-white course__array__button"
                    type="button"
                    onClick={() => handleAddOption(key)}
                  >
                    Add option
                  </button>
                </div>
              )}

              {metadataDefault[key] !== "Array" && (
                <select
                  className="course__field__input"
                  name={key}
                  value={savedData[key] || ""}
                  onChange={e => handleSelectChange(key, e.target.value)}
                >
                  <option value="" disabled>Select an option</option>
                  {metadataOptions[key].map((option, index) => (
                    <option key={index} value={option}>{option}</option>
                  ))}
                </select>
              )}
            </div>
          ))}
        </div>
      </div>
      <div className="button-row">
        <button className="btn-basic-black" onClick={onBack}>Back</button>
        <button className="btn-basic-black" onClick={onNext}>Continue</button>
      </div>
    </div>
  );
};

export default Metadata;
