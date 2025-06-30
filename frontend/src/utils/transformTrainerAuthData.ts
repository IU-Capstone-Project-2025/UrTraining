// src/utils/transformSurveyData.ts
type FlatFormData = { [key: string]: any };

export function transformToApiPayload(formData: FlatFormData) {
  const {
    level,
    sertification,
    specialization,
    training_location,
    years,
    gender,
    ...rest
  } = formData;

  return {
    trainer_profile: {
    profile_picture: "string",
    certification: {
      Type: sertification,
      Level: level,
      Specialization: specialization,
    },
    experience: {
      Years: years,
      Specialization: specialization,
      Courses: 0,
      Rating: 0,
    },
    badges: [
    ],
    reviews_count: 0,
    bio: "bio",
  }
  };
}
