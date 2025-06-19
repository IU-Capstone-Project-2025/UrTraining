import React from 'react'
import Survey from "../components/Survey"
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { example_survey_data } from "../components/data/example_json_data"
import SurveyPageContext from "../components/context/SurveyPageContext";
import type { SurveyContextType } from "../components/context/SurveyPageContext";

// Страница редактирования профиля пользователя, которая переиспользует компонент Survey для редактирования данных тренировочного профиля.
// Страница добавляет заголовок "Profile Settings" и модифицирует данные опроса (меняет title на "Edit Your Profile"),
// позволяя пользователю обновлять свою информацию через тот же интерфейс, что и при первоначальном заполнении анкеты,
// с автоматическим сохранением изменений при навигации по шагам.

const ProfileEditPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [surveyStep, setSurveyStep] = useState(0);

  useEffect(() => {
    let newStep = parseInt(searchParams.get('step') || '') || 1;

    if (newStep < 1 || newStep > example_survey_data.steps_total.length) {
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

  // Модифицируем данные опроса для редактирования профиля
  const profileEditData = {
    ...example_survey_data,
    title: "Edit Your Profile",
    information: {
      title: "Update Your Information",
      description: "You can update your profile information here. Changes will be saved automatically as you navigate through the steps."
    }
  };

  return (
    <div>
      <div style={{ 
        padding: '20px', 
        backgroundColor: '#f8f9fa', 
        borderBottom: '1px solid #dee2e6',
        marginBottom: '20px'
      }}>
        <h1 style={{ margin: 0, color: '#333' }}>Profile Settings</h1>
        <p style={{ margin: '5px 0 0 0', color: '#666' }}>
          Update your training profile information
        </p>
      </div>
      
      <SurveyPageContext value={contextValue}>
        <Survey {...profileEditData} />
      </SurveyPageContext>
    </div>
  )
}

export default ProfileEditPage 