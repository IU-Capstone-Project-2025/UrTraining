// src/utils/transformSurveyData.ts
type FlatFormData = { [key: string]: any };

export function transformToApiPayload(formData: FlatFormData) {
  const {
    name,
    surname,
    email,
    gender,
    age,
    height_cm,
    weight_kg,
    frequency_last_3_months,
    session_duration,
    restriction,
    joint_back_problems,
    chronic_conditions,
    health_details,
    location_details,
    training_location,
    ...rest
  } = formData;

  const training_goals = Object.keys(rest)
    .filter((key) => key.startsWith("training_goals"))
    .map((key) => rest[key])
    .filter(Boolean);

  const training_types = [
    "strength_training",
    "cardio",
    "hiit",
    "yoga_pilates",
    "functional_training",
    "stretching",
  ].reduce((acc, key) => {
    if (rest[key]) acc[key] = parseInt(rest[key], 10);
    return acc;
  }, {} as Record<string, number>);

  return {
    full_name: `${name} ${surname}`,
    email,
    training_profile: {
      basic_information: {
        gender,
        age: Number(age),
        height_cm: Number(height_cm),
        weight_kg: Number(weight_kg),
      },
      training_goals,
      training_experience: {
        level: "beginner",
        frequency_last_3_months,
      },
      preferences: {
        training_location,
        location_details,
        session_duration,
      },
      health: {
        joint_back_problems: joint_back_problems === "true",
        chronic_conditions: chronic_conditions === "true",
        health_details,
      },
      training_types,
    },
  };
}
