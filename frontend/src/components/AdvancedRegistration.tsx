import React, { useContext, useState } from 'react'
import type { StepsTotal, SurveyOption, SurveyStep } from './interface/surveyInterface';
import SurveyPageContext from './context/SurveyPageContext';
import { InputTemplates } from './InputTemplates'
import "../css/Survey.css"
import type { InputField } from './interface/interfaces';
import AuthContext from './context/AuthContext';
import { useNavigate } from 'react-router-dom';

interface StepData {
    [key: string]: any;
}

const AdvancedRegistration = (props: SurveyStep) => {
    const [savedData, setSavedData] = useState<StepData>({})
    const [isSubmitting, setIsSubmitting] = useState(false);
    const stepContext = useContext(SurveyPageContext)

    const navigate = useNavigate();

    // Get first and last step
    const first_step = props.steps_total[0].value
    const last_step = props.steps_total[props.steps_total.length - 1].value

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
            <div className="survey__navbar">
                {props.steps_total.map((step: StepsTotal, value: number) => {
                    return (
                        <h3 key={value} className={step.value === props.step_current ? "survey__navbar__selected" : ""}>
                            {step.placeholder}
                        </h3>
                    )
                })}
            </div>

            <div className="survey__container">
                <div className="survey__options">
                    <div className="survey__title">
                        {props.title}
                    </div>
                    {props.options.map((options_page: SurveyOption, value: number) => {
                        return (
                            <div key={value} className="survey__options__section">
                                <p>
                                    {options_page.subtitle}
                                </p>
                                <div className="survey__section__forms">
                                    <form onChange={handleChange}>
                                        {options_page.inputs.map((input_option: InputField, value: number) => {
                                            return (
                                                <InputTemplates key={value} {...input_option} />
                                            )
                                        })}
                                    </form>
                                </div>
                            </div>
                        )
                    })}
                </div>

                <div className="survey__info">
                    <div className="survey__info__description">
                        <div className="survey__title">
                            <h2>
                                {props.information.title}
                            </h2>
                        </div>
                        <p>
                            {props.information.description}
                        </p>
                    </div>
                    <div className="survey__info__button">
                        {
                            props.step_current !== first_step ?
                                <button className="btn-basic-black" onClick={handleBack}>
                                    Back
                                </button> : ""
                        }

                        {
                            props.step_current !== last_step ?
                                <button className="btn-basic-black" onClick={handleContinue}>
                                    Continue
                                </button> : ""
                        }

                        {
                            props.step_current === last_step ?
                                <button className="btn-basic-black" onClick={handleSubmit}>
                                    Submit
                                </button> : ""
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}

export default AdvancedRegistration