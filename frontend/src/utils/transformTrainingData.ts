// src/utils/transformSurveyData.ts
import { trainerDataRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";

type FlatFormData = { [key: string]: any };

export function formatTrainingData(formData: FlatFormData, trainerData: FlatFormData) {
  const {
    activity_type,
    program_goal,
    training_environment,
    difficulty_level,
    course_duration,
    weekly_training_frequency,
    average_workout_duration,
    age_group,
    gender_orientation,
    physical_limitations,
    required_equipment,
    course_language,
    visual_content,
    tags,
    course_title,
    program_description,
    training_plan,
    ...rest
  } = formData;

  return {
    "Activity Type": activity_type,
    "Program Goal": program_goal,
    "Training Environment": training_environment,
    "Difficulty Level": difficulty_level,
    "Course Duration (weeks)": course_duration,
    "Weekly Training Frequency": weekly_training_frequency,
    "Average Workout Duration": average_workout_duration,
    "Age Group": age_group,
    "Gender Orientation": gender_orientation,
    "Physical Limitations": physical_limitations,
    "Required Equipment": required_equipment,
    "Course Language": course_language,
    "Visual Content": [
      "None"
    ],
    "Trainer Feedback Options": [
      "None"
    ],
    "Tags": tags,
    "Average Course Rating": 0,
    "Active Participants": 0,
    "Number of Reviews": 0,
    "Certification": trainerData.trainer_profile.certification,
    "Experience": trainerData.trainer_profile.experience,
    "Trainer Name": "string",
    "Course Title": course_title,
    "Program Description": program_description,
    "training_plan": training_plan
  };
}
