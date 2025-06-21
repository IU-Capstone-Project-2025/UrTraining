// import React from 'react'
import Survey from "../components/Survey"
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { example_survey_data } from "../components/data/example_json_data"
import SurveyPageContext from "../components/context/SurveyPageContext";
import type { SurveyContextType } from "../components/context/SurveyPageContext";
import { sanitizeSurveyData } from "../utils/sanitizeSurveyData";
import type { SurveyProps} from "../components/interface/interfaces";
import axios from 'axios';

const SurveyPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [surveyStep, setSurveyStep] = useState(1);
  const [fullSurveyData, setFullSurveyData] = useState<SurveyProps[]>([]);

  useEffect(() => {
    console.log("mgeeeeeeeeeee");

    let newStep = parseInt(searchParams.get('step') || '') || 1;

    if (newStep < 1 || newStep > 4) {
      newStep = 1;
      setSearchParams({ step: newStep.toString() }, { replace: true });
    }    

    console.log(newStep);
    

    setSurveyStep(newStep);
  }, [searchParams]);

  useEffect(() => {
    const fetchAllSurveyData = async () => {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/survey-data`);
        console.log("Survey data received:", res.data);
        setFullSurveyData(res.data);
      } catch (error) {
        console.error("Error fetching survey data:", error);
      }
    };

    fetchAllSurveyData();
  }, []);

  const updateStep = (newStep: number) => {
    setSearchParams({ step: newStep.toString() });
  };

  const contextValue: SurveyContextType = {
    currentStep: surveyStep,
    updateStep,
  };

  if (fullSurveyData.length == 0) {
    return <div>Loading step data...</div>;
  }
  else {
    const currentStepData = fullSurveyData.find(
      (item) => item.step_current === `step-${surveyStep}`
    );

    const cleanedData = sanitizeSurveyData(currentStepData);

    return (
    <SurveyPageContext value={contextValue}>
      <Survey {...cleanedData} />
    </SurveyPageContext>
    )
  }
}

export default SurveyPage