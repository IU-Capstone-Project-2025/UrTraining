import React, { useContext } from 'react'
import { useState, useEffect } from 'react';
import type { SurveyProps, SurveyOption, SurveyStep, InputField } from "../components/interface/interfaces";
import SurveyPageContext from './context/SurveyPageContext';
import { InputTemplates } from './InputTemplates'
import "../css/Survey.css"

interface StepData {
    [key: string]: any;
}

const Survey = (props: SurveyProps) => {
    const [savedData, setSavedData] = useState<StepData>({});

    const stepContext = useContext(SurveyPageContext)

    const first_step = props.steps_total[0].value
    const last_step = props.steps_total[props.steps_total.length - 1].value

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setSavedData(prev => ({ ...prev, [name]: value }));
    };

    const handleContinue = () => {
        console.log(savedData);
        stepContext.updateStep(stepContext.currentStep + 1)
    }


    return (
        <div className="survey basic-page">
            <div className="survey__navbar">
                {props.steps_total.map((step: SurveyStep, value: number) => {
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
                                <button className="btn-basic-black">
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
                                <button className="btn-basic-black">
                                    Submit
                                </button> : ""
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Survey