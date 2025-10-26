import React, { useEffect, useMemo } from 'react';
//import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';
import AuthContext from "../components/context/AuthContext";
import { trainingsDataRequest, userInfoRequest, getAllTrainingProgress, getSavedCoursesRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { data, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const CoursesCataloguePage = React.memo(() => {

  const authData = useContext(AuthContext)
  const navigate = useNavigate();
  const { t } = useTranslation();

  const emptyArray = useMemo(() => [], []);

  const { data: trainingsData = emptyArray, isLoading, status } = useQuery<any, Error>({
    queryKey: ['formTrainings'],
    queryFn: () => trainingsDataRequest(authData.access_token),
    staleTime: 5 * 60 * 1000, // 5 минут
    refetchOnWindowFocus: false,
  })

  // vvvvvvvvvvvv
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // vvvvvvvvvvvv

  const { data: userData, isLoading: userDataIsLoading, status: userDataStatus } = useQuery({
    queryKey: ['me'],
    queryFn: () => userInfoRequest(authData.access_token),
    enabled: authData.access_token !== "",
    staleTime: 5 * 60 * 1000, // 5 минут
    refetchOnWindowFocus: false,
  })

  // Get user's progress data
  const { data: progressData = [], isLoading: progressLoading } = useQuery({
    queryKey: ['allProgress'],
    queryFn: () => getAllTrainingProgress(authData.access_token),
    enabled: authData.access_token !== "",
    staleTime: 2 * 60 * 1000, // 2 минуты
    refetchOnWindowFocus: false,
  })

  // Get user's saved courses
  const { data: savedCourses = [], isLoading: savedLoading } = useQuery({
    queryKey: ['savedCourses'],
    queryFn: () => getSavedCoursesRequest(authData.access_token),
    enabled: authData.access_token !== "",
    staleTime: 2 * 60 * 1000, // 2 минуты
    refetchOnWindowFocus: false,
  })

  useEffect(() => {
    if (userData === undefined)
      navigate("/signin")
  })

  const title = {
    title_top: t("catalogue.title_top"), 
    title_bottom: t("catalogue.title_bottom")
  };

  if (isLoading) {
    return <div className="centered-content">
      <div className="step-title-main">{t("catalogue.loading")}</div>
      <p>{t("catalogue.load_desc")}</p>
    </div>;
  }

  return (
    <>
      <CourseCatalogue 
        courses={trainingsData} 
        title={title}
        progressData={progressData}
        savedCourses={savedCourses}
      />
    </>
  );
});

export default CoursesCataloguePage;