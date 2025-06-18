// import React from 'react'
import Survey from "../components/Survey"
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { example_survey_data } from "../components/data/example_json_data"

const SurveyPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [step, setStep] = useState(1);

  useEffect(() => {
    let newStep = parseInt(searchParams.get('step') || '') || 1;

    if (newStep < 1 || newStep > 4) {
      newStep = 1;
      setSearchParams({ step: newStep.toString() }, { replace: true });
    }

    setStep(newStep);
  }, [searchParams]);

  const updateStep = (newStep: number) => {
    setSearchParams({ step: newStep.toString() });
  };

  return (
    <Survey
      {...example_survey_data}
    />
  )
}

export default SurveyPage