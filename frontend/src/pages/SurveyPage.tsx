// import React from 'react'
import Survey from "../components/Survey"
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { example_survey_data } from "../components/data/example_json_data"
import SurveyPageContext from "../components/context/SurveyPageContext";
import type { SurveyContextType } from "../components/context/SurveyPageContext";

const SurveyPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [surveyStep, setSurveyStep] = useState(0);

  useEffect(() => {
    let newStep = parseInt(searchParams.get('step') || '') || 1;

    if (newStep < 1 || newStep > 4) {
      newStep = 1;
      setSearchParams({ step: newStep.toString() }, { replace: true });
    }

    setSurveyStep(newStep);
  }, [searchParams]);

  const updateStep = (newStep: number) => {
    setSearchParams({ step: newStep.toString() });
  };

  const contextValue: SurveyContextType = {
    currentStep: surveyStep,
    updateStep,
  };

  return (
    <SurveyPageContext value={contextValue}>
      <Survey {...example_survey_data} />
    </SurveyPageContext>
  )
}

export default SurveyPage