// Type for defining type of input provided
export type InputType = "text" | "number" | "email" | "password" | "select" | "radio" | "scale";

// "Templates" of how data should be received from API
export interface SignProps {
    user_exists: boolean;
    image_path: string;
    page_title: string;
    input_fields: InputField[];
    social_links: SocialLink[];
}

export interface SurveyProps {
    steps_total: SurveyStep[];
    step_current: string;
    title: string;
    options: SurveyOption[];
    information: SurveyInformation;
}

// Basic interface for any form

export interface InputField {
    name: string;
    id: string;
    input_type: InputType;
    placeholder: string;
    options: SelectOption[] | "";
}

// Other interfaces

export interface SelectOption {
    id: string;
    name: string;
    value: string;
    placeholder: string;
}

export interface SurveyStep {
    value: string;
    placeholder: string;
}

export interface SurveyOption {
    subtitle: string;
    inputs: InputField[];
}

export interface SurveyInformation {
    title: string;
    description: string;
}

export interface SocialLink {
    name: string;
    placeholder: string;
}
