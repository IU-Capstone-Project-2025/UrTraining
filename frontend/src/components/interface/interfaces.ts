// Type for defining type of input provided
export type InputType =
    | "text"
    | "number"
    | "email"
    | "password"
    | "select"
    | "radio";

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

export interface SignInSuccess {
    access_token: string;
    token_type: string;
    expires_in: number;
    user_info: {
        additionalProp1: {};
    };
}

export interface UserProps {
    
}

export interface SignInFailed {
    detail: [
        {
            loc: [string, number];
            msg: string;
            type: string;
        }
    ];
}

export interface SignUpSuccess {
    message: string;
    user_info: {
        additionalProp1: {};
    };
}

export interface SignUpFailed {
    detail: [
        {
            loc: [string, number];
            msg: string;
            type: string;
        }
    ];
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

export interface CredentialsData {
    username: String;
    email: String;
    password: String;
    full_name: String;
}

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
