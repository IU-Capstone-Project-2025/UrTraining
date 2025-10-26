import type { SignProps } from "../interface/interfaces";
import type { TFunction } from "i18next";

export const example_survey_data = (t: TFunction): any => ({
    steps_total: [
        {
            value: "step-1",
            placeholder: "Step 1",
        },
        {
            value: "step-2",
            placeholder: "Step 2",
        },
        {
            value: "step-3",
            placeholder: "Step 3",
        },
        {
            value: "step-4",
            placeholder: "Step 4",
        },
    ],
    step_current: "step-1",
    title: "Let's know each other",
    options: [
        {
            subtitle: "How can we call you?",
            inputs: [
                {
                    name: "name",
                    id: "name",
                    input_type: "text",
                    placeholder: "Name",
                    options: [],
                },
                {
                    name: "surname",
                    id: "surname",
                    input_type: "text",
                    placeholder: "Surname",
                    options: [],
                },
            ],
        },
        {
            subtitle: "Where are you from?",
            inputs: [
                {
                    name: "country",
                    id: "country",
                    input_type: "select",
                    placeholder: "Country",
                    options: [
                        {
                            id: "kz",
                            name: "kazakhstan",
                            value: "kz",
                            placeholder: "Kazakhstan",
                        },
                        {
                            id: "ru",
                            name: "russia",
                            value: "ru",
                            placeholder: "Russia",
                        },
                        {
                            id: "us",
                            name: "usa",
                            value: "us",
                            placeholder: "United States",
                        },
                    ],
                },
                {
                    name: "city",
                    id: "city",
                    input_type: "text",
                    placeholder: "City",
                    options: [],
                },
            ],
        },
        {
            subtitle: "What is your gender?",
            inputs: [
                {
                    name: "gender",
                    id: "gender",
                    input_type: "radio",
                    placeholder: "Gender",
                    options: [
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
            ],
        },
        {
            subtitle: "More data",
            inputs: [
                {
                    name: "age",
                    id: "age",
                    input_type: "number",
                    placeholder: "Age",
                    options: [],
                },
                {
                    name: "height",
                    id: "height",
                    input_type: "number",
                    placeholder: "Height",
                    options: [],
                },
                {
                    name: "weight_kg",
                    id: "weight_kg",
                    input_type: "number",
                    placeholder: "Weight",
                    options: [],
                }
            ],
        },
    ],
    information: {
        title: "Why we collect your data?",
        description:
            "Before we dive into training, we’d love to get to know you better. Your name and a few basic details help us personalize your journey — like a good coach who remembers your story from day one.",
    },
});

export const example_signin_data = (t: TFunction): SignProps => ({
    user_exists: true,
    image_path: "images/signin_image.jpg",
    page_title: t("signin_data.title"),
    input_fields: [
        {
            name: "email",
            id: "email",
            input_type: "text",
            placeholder: t("signin_data.email"),
            options: [],
        },
        {
            name: "password",
            id: "password",
            input_type: "password",
            placeholder: t("signin_data.password"),
            options: [],
        },
    ],
    social_links: [
        {
            name: "google-socials",
            placeholder: t("signin_data.google"),
        },
        {
            name: "telegram-socials",
            placeholder: t("signin_data.telegram"),
        },
    ],
});

export const example_signup_data = (t: TFunction): SignProps => ({
    user_exists: false,
    image_path: "images/signup_image.jpg",
    page_title: t("signup_data.title"),
    input_fields: [
        {
            name: "username",
            id: "username",
            input_type: "text",
            placeholder: t("signup_data.username"),
            options: [],
        },
        {
            name: "email",
            id: "email",
            input_type: "email",
            placeholder: t("signup_data.email"),
            options: [],
        },
        {
            name: "password",
            id: "password",
            input_type: "password",
            placeholder: t("signup_data.password"),
            options: [],
        },
    ],
    social_links: [
        {
            name: "google-socials",
            placeholder: t("signup_data.google"),
        },
        {
            name: "telegram-socials",
            placeholder: t("signup_data.telegram"),
        },
    ],
});
