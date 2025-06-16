// import React from 'react'
import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import "../css/Survey.css"
import Step1Survey from './survey/Step1Survey';

const Survey = () => {
    const [searchParams, setSearchParams] = useSearchParams();

    const step = parseInt(searchParams.get('step') || '') || 1;

    useEffect(() => {
        if (step < 1 || step > 4) {
            goToStep(1);
        }
    }, [step]);

    const goToStep = (newStep: Number) => {
        setSearchParams({ step: newStep.toString() });
    };

    return (
        <div className="survey basic-page">
            <div className="survey__navbar">
                {[1, 2, 3, 4].map((s) => <h3 className={step === s ? "survey__navbar__selected" : ""}>Step {s}</h3>)}
            </div>
            <div className="survey__container">
                <div className="survey__options">
                    {step === 1 && <Step1Survey />}
                </div>
                <div className="survey__info">
                    <div className="survey__info__description">
                        {step === 1 &&
                            <>
                                <div className="survey__title">
                                    <h2>
                                        Why we collect your data?
                                    </h2>
                                </div>
                                <p>
                                    Idk lol, why do you ask? Just agree with our TOS and let machine process your precious data.
                                    You don't care anyways.
                                </p>
                            </>
                        }
                    </div>
                    <div className="survey__info__button">
                        {step !== 1 &&
                            <>
                                <button className="btn-basic-black" onClick={() => goToStep(step - 1)}>
                                    Back
                                </button>
                            </>
                        }
                        {step !== 4 &&
                            <>
                                <button className="btn-basic-black" onClick={() => goToStep(step + 1)}>
                                    Continue
                                </button>
                            </>
                        }
                        {step === 4 &&
                            <>
                                <button className="btn-basic-black">
                                    Submit
                                </button>
                            </>
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Survey