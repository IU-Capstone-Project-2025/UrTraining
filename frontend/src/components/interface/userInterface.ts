export interface UserProp {
  user_info: UserInfo
}

export interface UserInfo {
  id: number
  username: string
  email: string
  full_name: string
  is_admin: boolean
  created_at: string
  updated_at: any
  training_profile: TrainingProfile
}

export interface TrainingProfile {
  basic_information: BasicInformation
  training_goals: string[]
  training_experience: TrainingExperience
  preferences: Preferences
  health: Health
  training_types: TrainingTypes
}

export interface BasicInformation {
  gender: string
  age: number
  height_cm: number
  weight_kg: number
}

export interface TrainingExperience {
  level: string
  frequency_last_3_months: string
}

export interface Preferences {
  training_location: string
  location_details: string
  session_duration: string
}

export interface Health {
  joint_back_problems: boolean
  chronic_conditions: boolean
  health_details: any
}

export interface TrainingTypes {
  strength_training: number
  cardio: number
  hiit: number
  yoga_pilates: number
  functional_training: number
  stretching: number
}
