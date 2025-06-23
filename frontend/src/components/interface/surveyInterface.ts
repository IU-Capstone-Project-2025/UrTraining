import type { InputField } from "./interfaces"

export type SurveyProp = SurveyStep[]

export interface SurveyStep { // SurveyProps
  steps_total: StepsTotal[]
  step_current: string
  title: string
  options: SurveyOption[]
  information: SurveyInformation
}

export interface StepsTotal { // SurveyStep
  value: string
  placeholder: string
}

export interface SurveyOption { // SurveyOption
  subtitle: string
  inputs: InputField[]
}

export interface SurveyInformation { // SurveyInformation
  title: string
  description: string
}