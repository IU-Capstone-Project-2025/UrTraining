import type { SurveyProps, SignProps } from "../interface/interfaces";

export const example_survey_data: SurveyProps = {
    steps_total: [
        {
            value: "step-1",
            placeholder: "Personal Info",
        },
        {
            value: "step-2",
            placeholder: "Basic Data",
        },
        {
            value: "step-3",
            placeholder: "Goals",
        },
        {
            value: "step-4",
            placeholder: "Experience",
        },
        {
            value: "step-5",
            placeholder: "Preferences",
        },
        {
            value: "step-6",
            placeholder: "Health & Types",
        },
    ],
    step_current: "step-1",
    title: "Let's know each other",
    options: [
        // Step 1: Personal Info
        {
            subtitle: "Personal Information",
            inputs: [
                {
                    name: "name",
                    id: "name",
                    input_type: "text",
                    label: "First Name",
                    placeholder: "Enter your first name",
                    options: "",
                },
                {
                    name: "surname",
                    id: "surname",
                    input_type: "text",
                    label: "Last Name",
                    placeholder: "Enter your last name",
                    options: "",
                },
                {
                    name: "country",
                    id: "country",
                    input_type: "select",
                    label: "Country",
                    placeholder: "Select your country",
                    options: [
                        {
                            id: "kz",
                            name: "country",
                            value: "kz",
                            placeholder: "Kazakhstan",
                        },
                        {
                            id: "ru",
                            name: "country",
                            value: "ru",
                            placeholder: "Russia",
                        },
                        {
                            id: "us",
                            name: "country",
                            value: "us",
                            placeholder: "United States",
                        },
                    ],
                },
                {
                    name: "city",
                    id: "city",
                    input_type: "text",
                    label: "City",
                    placeholder: "Enter your city",
                    options: "",
                },
            ],
        },
        // Step 2: Basic Data
        {
            subtitle: "Basic Physical Information",
            inputs: [
                {
                    name: "gender",
                    id: "gender",
                    input_type: "select",
                    label: "Gender",
                    placeholder: "Select your gender",
                    options: [
                        {
                            id: "not_selected",
                            name: "gender",
                            value: "",
                            placeholder: "Не выбрано",
                        },
                        {
                            id: "male",
                            name: "gender",
                            value: "male",
                            placeholder: "Male",
                        },
                        {
                            id: "female",
                            name: "gender",
                            value: "female",
                            placeholder: "Female",
                        },
                    ],
                },
                {
                    name: "age",
                    id: "age",
                    input_type: "number",
                    label: "Age",
                    placeholder: "Enter your age in years",
                    options: "",
                    validation: {
                        min: 13,
                        max: 100,
                        required: true,
                        errorMessage: "Age must be between 13 and 100 years"
                    }
                },
                {
                    name: "height",
                    id: "height",
                    input_type: "number",
                    label: "Height",
                    placeholder: "Enter your height in cm",
                    options: "",
                    validation: {
                        min: 100,
                        max: 250,
                        required: true,
                        errorMessage: "Height must be between 100 and 250 cm"
                    }
                },
                {
                    name: "weight",
                    id: "weight",
                    input_type: "number",
                    label: "Weight",
                    placeholder: "Enter your weight in kg",
                    options: "",
                    validation: {
                        min: 30,
                        max: 300,
                        required: true,
                        errorMessage: "Weight must be between 30 and 300 kg"
                    }
                },
            ],
        },
        // Step 3: Goals
        {
            subtitle: "What are your training goals?",
            inputs: [
                {
                    name: "training_goals",
                    id: "training_goals",
                    input_type: "checkbox",
                    label: "Training Goals",
                    placeholder: "Select your training goals",
                    options: [
                        {
                            id: "weight_loss",
                            name: "training_goals",
                            value: "weight_loss",
                            placeholder: "Weight Loss",
                        },
                        {
                            id: "muscle_gain",
                            name: "training_goals",
                            value: "muscle_gain",
                            placeholder: "Muscle Gain",
                        },
                        {
                            id: "strength",
                            name: "training_goals",
                            value: "strength",
                            placeholder: "Increase Strength",
                        },
                        {
                            id: "endurance",
                            name: "training_goals",
                            value: "endurance",
                            placeholder: "Improve Endurance",
                        },
                        {
                            id: "flexibility",
                            name: "training_goals",
                            value: "flexibility",
                            placeholder: "Increase Flexibility",
                        },
                        {
                            id: "general_fitness",
                            name: "training_goals",
                            value: "general_fitness",
                            placeholder: "General Fitness",
                        },
                    ],
                },
            ],
        },
        // Step 4: Experience
        {
            subtitle: "Tell us about your training experience",
            inputs: [
                {
                    name: "training_level",
                    id: "training_level",
                    input_type: "select",
                    label: "Training Level",
                    placeholder: "Select your training level",
                    options: [
                        {
                            id: "beginner",
                            name: "training_level",
                            value: "beginner",
                            placeholder: "Beginner (0-6 months)",
                        },
                        {
                            id: "intermediate",
                            name: "training_level",
                            value: "intermediate",
                            placeholder: "Intermediate (6 months - 2 years)",
                        },
                        {
                            id: "advanced",
                            name: "training_level",
                            value: "advanced",
                            placeholder: "Advanced (2+ years)",
                        },
                    ],
                },
                {
                    name: "frequency_last_3_months",
                    id: "frequency_last_3_months",
                    input_type: "select",
                    label: "Training Frequency (Last 3 months)",
                    placeholder: "Select your training frequency",
                    options: [
                        {
                            id: "never",
                            name: "frequency_last_3_months",
                            value: "never",
                            placeholder: "Never",
                        },
                        {
                            id: "rarely",
                            name: "frequency_last_3_months",
                            value: "rarely",
                            placeholder: "1-2 times per month",
                        },
                        {
                            id: "sometimes",
                            name: "frequency_last_3_months",
                            value: "sometimes",
                            placeholder: "1-2 times per week",
                        },
                        {
                            id: "regularly",
                            name: "frequency_last_3_months",
                            value: "regularly",
                            placeholder: "3-4 times per week",
                        },
                        {
                            id: "very_often",
                            name: "frequency_last_3_months",
                            value: "very_often",
                            placeholder: "5+ times per week",
                        },
                    ],
                },
            ],
        },
        // Step 5: Preferences
        {
            subtitle: "Training preferences",
            inputs: [
                {
                    name: "training_location",
                    id: "training_location",
                    input_type: "select",
                    label: "Preferred Training Location",
                    placeholder: "Select your preferred location",
                    options: [
                        {
                            id: "home",
                            name: "training_location",
                            value: "home",
                            placeholder: "Home",
                        },
                        {
                            id: "gym",
                            name: "training_location",
                            value: "gym",
                            placeholder: "Gym",
                        },
                        {
                            id: "outdoor",
                            name: "training_location",
                            value: "outdoor",
                            placeholder: "Outdoor",
                        },
                        {
                            id: "mixed",
                            name: "training_location",
                            value: "mixed",
                            placeholder: "Mixed",
                        },
                    ],
                },
                {
                    name: "session_duration",
                    id: "session_duration",
                    input_type: "select",
                    label: "Preferred Session Duration",
                    placeholder: "Select session duration",
                    options: [
                        {
                            id: "15_30",
                            name: "session_duration",
                            value: "15_30",
                            placeholder: "15-30 minutes",
                        },
                        {
                            id: "30_45",
                            name: "session_duration",
                            value: "30_45",
                            placeholder: "30-45 minutes",
                        },
                        {
                            id: "45_60",
                            name: "session_duration",
                            value: "45_60",
                            placeholder: "45-60 minutes",
                        },
                        {
                            id: "60_plus",
                            name: "session_duration",
                            value: "60_plus",
                            placeholder: "60+ minutes",
                        },
                    ],
                },
                {
                    name: "location_details",
                    id: "location_details",
                    input_type: "textarea",
                    label: "Location Details",
                    placeholder: "Additional details about your training location or equipment (optional)",
                    options: "",
                },
            ],
        },
        // Step 6: Health & Types
        {
            subtitle: "Health information and training types",
            inputs: [
                {
                    name: "joint_back_problems",
                    id: "joint_back_problems",
                    input_type: "select",
                    label: "Joint or Back Problems",
                    placeholder: "Do you have any joint or back problems?",
                    options: [
                        {
                            id: "joint_not_selected",
                            name: "joint_back_problems",
                            value: "",
                            placeholder: "Не выбрано",
                        },
                        {
                            id: "joint_yes",
                            name: "joint_back_problems",
                            value: "true",
                            placeholder: "Yes",
                        },
                        {
                            id: "joint_no",
                            name: "joint_back_problems",
                            value: "false",
                            placeholder: "No",
                        },
                    ],
                },
                {
                    name: "chronic_conditions",
                    id: "chronic_conditions",
                    input_type: "select",
                    label: "Chronic Health Conditions",
                    placeholder: "Do you have any chronic health conditions?",
                    options: [
                        {
                            id: "chronic_not_selected",
                            name: "chronic_conditions",
                            value: "",
                            placeholder: "Не выбрано",
                        },
                        {
                            id: "chronic_yes",
                            name: "chronic_conditions",
                            value: "true",
                            placeholder: "Yes",
                        },
                        {
                            id: "chronic_no",
                            name: "chronic_conditions",
                            value: "false",
                            placeholder: "No",
                        },
                    ],
                },
                {
                    name: "health_details",
                    id: "health_details",
                    input_type: "textarea",
                    label: "Health Details",
                    placeholder: "Please describe any health conditions or concerns (optional)",
                    options: "",
                },
                {
                    name: "strength_training",
                    id: "strength_training",
                    input_type: "rating",
                    label: "Strength Training",
                    placeholder: "Rate your interest in strength training",
                    options: "",
                    validation: {
                        min: 1,
                        max: 5,
                        required: true,
                        errorMessage: "Please rate your interest from 1 to 5"
                    }
                },
                {
                    name: "cardio",
                    id: "cardio",
                    input_type: "rating",
                    label: "Cardio",
                    placeholder: "Rate your interest in cardio exercises",
                    options: "",
                    validation: {
                        min: 1,
                        max: 5,
                        required: true,
                        errorMessage: "Please rate your interest from 1 to 5"
                    }
                },
                {
                    name: "hiit",
                    id: "hiit",
                    input_type: "rating",
                    label: "HIIT (High-Intensity Interval Training)",
                    placeholder: "Rate your interest in HIIT workouts",
                    options: "",
                    validation: {
                        min: 1,
                        max: 5,
                        required: true,
                        errorMessage: "Please rate your interest from 1 to 5"
                    }
                },
                {
                    name: "yoga_pilates",
                    id: "yoga_pilates",
                    input_type: "rating",
                    label: "Yoga/Pilates",
                    placeholder: "Rate your interest in yoga or pilates",
                    options: "",
                    validation: {
                        min: 1,
                        max: 5,
                        required: true,
                        errorMessage: "Please rate your interest from 1 to 5"
                    }
                },
                {
                    name: "functional_training",
                    id: "functional_training",
                    input_type: "rating",
                    label: "Functional Training",
                    placeholder: "Rate your interest in functional training",
                    options: "",
                    validation: {
                        min: 1,
                        max: 5,
                        required: true,
                        errorMessage: "Please rate your interest from 1 to 5"
                    }
                },
                {
                    name: "stretching",
                    id: "stretching",
                    input_type: "rating",
                    label: "Stretching",
                    placeholder: "Rate your interest in stretching exercises",
                    options: "",
                    validation: {
                        min: 1,
                        max: 5,
                        required: true,
                        errorMessage: "Please rate your interest from 1 to 5"
                    }
                },
            ],
        },
    ],
    information: {
        title: "Why we collect your data?",
        description:
            "Idk lol, why do you ask? Just agree with our TOS and let machine process your precious data. You don't care anyways.",
    },
};

export const example_signin_data: SignProps = {
    user_exists: true,
    image_path: "images/signin_image.jpg",
    page_title: "Welcome back!",
    input_fields: [
        {
            name: "username",
            id: "username",
            input_type: "text",
            label: "Username",
            placeholder: "Enter your username",
            options: "",
        },
        {
            name: "password",
            id: "password",
            input_type: "password",
            label: "Password",
            placeholder: "Enter your password",
            options: "",
        },
    ],
    social_links: [
        {
            name: "google-socials",
            placeholder: "Sign In with Google",
        },
        {
            name: "telegram-socials",
            placeholder: "Sign In with Telegram",
        },
    ],
};

export const example_signup_data: SignProps = {
    user_exists: false,
    image_path: "images/signup_image.jpg",
    page_title: "Sign Up",
    input_fields: [
        {
            name: "username",
            id: "username",
            input_type: "text",
            label: "Username",
            placeholder: "Choose a username",
            options: "",
        },
        {
            name: "email",
            id: "email",
            input_type: "email",
            label: "Email",
            placeholder: "Enter your email address",
            options: "",
        },
        {
            name: "password",
            id: "password",
            input_type: "password",
            label: "Password",
            placeholder: "Create a password",
            options: "",
        },
    ],
    social_links: [
        {
            name: "google-socials",
            placeholder: "Sign Up with Google",
        },
        {
            name: "telegram-socials",
            placeholder: "Sign Up with Telegram",
        },
    ],
};
