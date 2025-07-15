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

const NavButtons = (props: SurveyStep, handleBack: any, handleContinue: any, handleSubmit: any) => {
    // Get first and last step
    const first_step = props.steps_total[0].value
    const last_step = props.steps_total[props.steps_total.length - 1].value

    return (<>
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

        {
            props.step_current !== first_step ?
                <button className="btn-basic-black" onClick={handleBack}>
                    Back
                </button> : ""
        }
    </>)
}

const Survey = (props: SurveyStep) => {
    const [savedData, setSavedData] = useState<StepData>({})
    const [isSubmitting, setIsSubmitting] = useState(false);
    const stepContext = useContext(SurveyPageContext)

    const navigate = useNavigate();

    const handleContinue = () => {
        stepContext.updateStep(stepContext.currentStep + 1)
        const el = document.getElementById('root');
        if (el) {
            el.scrollIntoView({ behavior: "smooth" });
        }
    }

    const handleBack = () => {
        stepContext.updateStep(stepContext.currentStep - 1)
        const el = document.getElementById('root');
        if (el) {
            el.scrollIntoView({ behavior: "smooth" });
        }
    }

    const handleSubmit = async () => {
        setIsSubmitting(true);
        console.log(savedData);
        console.log("Handle submit call");
        try {
            await stepContext.submitSurvey(savedData);
            navigate('/recommendations');
        } catch (err) {
            console.error("Ошибка отправки:", err);
        } finally {
            setIsSubmitting(false);
        }
        navigate('/recommendations');
    }

    const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
        const target = event.target as HTMLInputElement;
        const { name, value } = target;
        setSavedData(prev => ({ ...prev, [name]: value }));
    };

    return (
        <div className="survey basic-page">
            <div className="survey__box">

                <div className="survey__navbar">
                    {props.steps_total.map((step: StepsTotal, value: number) => {
                        return (
                            <div key={value} className={step.value === props.step_current ? "survey__navbar__element survey__navbar__selected" : "survey__navbar__element"}>
                                <h3>{step.placeholder}</h3>
                            </div>
                        )
                    })}
                </div>

                <div className="survey__navbar survey__mobile">
                    {props.steps_total.map((step: StepsTotal, value: number) => {
                        return (
                            <div key={value} className={step.value === props.step_current ? "survey__navbar__element survey__navbar__selected" : "survey__navbar__element"}>
                                <h3>{step.value.substring(5)}</h3>
                            </div>
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
                            {NavButtons(props, handleBack, handleContinue, handleSubmit)}
                        </div>
                    </div>

                    <div className="survey__info">
                        <div style={{ position: "relative" }}>
                            <div className="assets__background__gradient" style={{ top: "0", left: "0" }}></div>
                        </div>
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
                            {NavButtons(props, handleBack, handleContinue, handleSubmit)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Survey