import React, { useContext, useEffect, useState } from 'react'
import type { StepsTotal, SurveyOption, SurveyStep } from './interface/surveyInterface';
import SurveyPageContext from './context/SurveyPageContext';
import { InputTemplates } from './InputTemplates'
import "../css/Survey.css"
import type { InputField } from './interface/interfaces';
import AuthContext from './context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

interface StepData {
    [key: string]: any;
}

const NavButtons = (props: SurveyStep, handleBack: any, handleContinue: any, handleSubmit: any) => {
    // Get first and last step
    const first_step = props.steps_total[0].value
    const last_step = props.steps_total[props.steps_total.length - 1].value

    const { t } = useTranslation();

    return (<>
        {
            props.step_current !== last_step ?
                <button className="btn-basic-black" onClick={handleContinue}>
                    {t("survey.continue")}
                </button> : ""
        }

        {
            props.step_current === last_step ?
                <button className="btn-basic-black" onClick={handleSubmit}>
                    {t("survey.submit")}
                </button> : ""
        }

        {
            props.step_current !== first_step ?
                <button className="btn-basic-black" onClick={handleBack}>
                    {t("survey.back")}
                </button> : ""
        }
    </>)
}

const AdvancedRegistration = (props: SurveyStep) => {
    const [savedData, setSavedData] = useState<StepData>({})
    const [isSubmitting, setIsSubmitting] = useState(false);
    const stepContext = useContext(SurveyPageContext);
    const { t, i18n } = useTranslation();

    const navigate = useNavigate();

    const [localizedForm, setLocalizedForm] = useState(props);
    
    useEffect(() => {
    // вызывать каждый раз, когда меняется язык
        setLocalizedForm(translateForm(props));
    }, [props, i18n.language, t]);

    const translateForm = (data: any): any => {
        if (Array.isArray(data)) {
        return data.map(item => translateForm(item));
        } else if (typeof data === "object" && data !== null) {
        const translated: Record<string, any> = {};

        for (const [key, value] of Object.entries(data)) {
            if (typeof value === "string") {
            // переводим только ключевые поля
            if (["title", "subtitle", "placeholder", "description"].includes(key)) {
                translated[key] = t(`survey_form.${value}`, { defaultValue: value });
            } else {
                translated[key] = value;
            }
            } else {
            translated[key] = translateForm(value);
            }
        }

        return translated;
        }

        return data;
    };

    const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
        const target = event.target as HTMLInputElement;
        const { name, value } = target;
        setSavedData(prev => ({ ...prev, [name]: value }));
    };

    const handleContinue = () => {
        stepContext.updateStep(stepContext.currentStep + 1)
    }

    const handleBack = () => {
        stepContext.updateStep(stepContext.currentStep - 1)
    }

    const handleSubmit = () => {
        setIsSubmitting(true);
        console.log(savedData);
        console.log("Handle submit call");
        stepContext.submitSurvey(savedData);
        navigate('/upload-training');
    }

    return (
        <div className="survey basic-page">

            <div className='survey__box'>

                <div className="survey__navbar">
                    {localizedForm.steps_total.map((step: StepsTotal, value: number) => {
                        return (
                            <div key={value} className={step.value === localizedForm.step_current ? "survey__navbar__element survey__navbar__selected" : "survey__navbar__element"}>
                                <h3>{step.placeholder}</h3>
                            </div>
                        )
                    })}
                </div>

                <div className="survey__navbar survey__mobile">
                    {localizedForm.steps_total.map((step: StepsTotal, value: number) => {
                        return (
                            <div key={value} className={step.value === localizedForm.step_current ? "survey__navbar__element survey__navbar__selected" : "survey__navbar__element"}>
                                <h3>{step.value.substring(5)}</h3>
                            </div>
                        )
                    })}
                </div>

                <div className="survey__container">
                    <div className="survey__options">
                        <div className="survey__title">
                            {localizedForm.title}
                        </div>
                        {localizedForm.options.map((options_page: SurveyOption, value: number) => {
                            return (
                                <div key={value} className="survey__options__section">
                                    <p>
                                        {options_page.subtitle}
                                    </p>
                                    <div className="survey__section__forms">
                                        <form onChange={handleChange}>
                                            {options_page.inputs.map((input_option: InputField, value: number) => {
                                                const fieldName = input_option.name;
                                                return (
                                                    <InputTemplates 
                                                        key={value} 
                                                        {...input_option} 
                                                        value={savedData[fieldName] || ""}
                                                        onChange={(e) => {
                                                            const { name, value } = e.target;
                                                            setSavedData(prev => ({ ...prev, [name]: value }));
                                                    }}
                                                    />
                                                )
                                            })}
                                        </form>
                                    </div>
                                </div>
                            )
                        })}
                        <div className="survey__info__button survey__mobile">
                            {NavButtons(localizedForm, handleBack, handleContinue, handleSubmit)}
                        </div>
                    </div>

                    <div className="survey__info">
                        <div style={{ position: "relative" }}>
                            <div className="assets__background__gradient" style={{ top: "0", left: "0", background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                            filter: 'url(#blurOval)' }}></div>
                        </div>
                        <div className="survey__info__description">
                            <div className="survey__title">
                                <h2>
                                    {localizedForm.information.title}
                                </h2>
                            </div>
                            <p>
                                {localizedForm.information.description}
                            </p>
                        </div>
                        <div className="survey__info__button">
                            {NavButtons(localizedForm, handleBack, handleContinue, handleSubmit)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default AdvancedRegistration