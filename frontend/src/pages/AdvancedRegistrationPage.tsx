// import React from 'react'
import AdvancedRegistration from "../components/AdvancedRegistration"
import { useState, useEffect, useContext, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import SurveyPageContext from "../components/context/SurveyPageContext";
import type { SurveyContextType } from "../components/context/SurveyPageContext";
import AuthContext from "../components/context/AuthContext";
import { useQuery } from "@tanstack/react-query";
import { coachAuthDataRequest } from "../api/apiRequests";
import type { SurveyProp, SurveyStep } from "../components/interface/surveyInterface";
import { useSubmitCoachData } from "../api/mutations";
import { transformToApiPayload } from "../utils/transformTrainerAuthData";

const AdvancedRegistrationPage = () => {
  const [searchParams, setSearchParams] = useSearchParams(); // Hook to store search bar argument (step)
  const [surveyStep, setSurveyStep] = useState<number>(1); // Hook to store current step
  
  const authData = useContext(AuthContext)
  const submitCoachDataMutation = useSubmitCoachData(authData.access_token)

  // Cached function to get current step
  const parseStep = useCallback((): number => {
    const stepParam = parseInt(searchParams.get('step') ?? '', 10);
    return stepParam >= 1 && stepParam <= 4 ? stepParam : 1;
  }, [searchParams]);

  // UseEffect to handle survey steps
  useEffect(() => {
    // Parse step from search bar
    const parsed = parseStep();
    setSurveyStep(parsed);

    // If out of bounds or missing, overwrite URL
    if (parsed.toString() !== searchParams.get('step')) {
      setSearchParams({ step: parsed.toString() }, { replace: true });
    }
  }, [searchParams, parseStep, setSearchParams]);

  const contextValue: SurveyContextType = {
    currentStep: surveyStep,
    updateStep: (newStep) => setSearchParams({ step: newStep.toString() }),
    submitSurvey: (data) => submitCoachDataHandler(data)
  };

  function submitCoachDataHandler(data: any){
    const formattedData = transformToApiPayload(data)
    console.log(formattedData);
    submitCoachDataMutation.mutate(formattedData)
  }

  // Receive an array of survey pages from API
  const { data: pagesData = [], isLoading, status } = useQuery<SurveyProp, Error>({
    queryKey: ['coachAuth'],
    queryFn: () => coachAuthDataRequest(authData.access_token)
  })

  // Grab correct page from array of received data
  const currentStepData = pagesData.find(
    (item) => item.step_current === `step-${surveyStep}`
  );

  // Convert found page to SurveyStep
  const stepData = currentStepData as SurveyStep

  return (
    isLoading ?
      <div>...Loading</div> :
      <SurveyPageContext value={contextValue}>
        <AdvancedRegistration {...stepData} />
      </SurveyPageContext>
  )
}

export default AdvancedRegistrationPage;