import React, { useEffect } from 'react';
//import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';
import AuthContext from "../components/context/AuthContext";
import { getMyTrainingsRequest, getSavedCoursesRequest, userInfoRequest, getAllTrainingProgress } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { data, useNavigate } from 'react-router-dom';

const SavedCoursesPage = () => {

  const authData = useContext(AuthContext)
  const navigate = useNavigate();

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
    enabled: authData.access_token !== ""
  })

  const { data: trainingsData = [], isLoading, status } = useQuery<any, Error>({
    queryKey: ['savedCourses'],
    queryFn: () => getSavedCoursesRequest(authData.access_token),
    enabled: userData !== null,
    staleTime: 0, // Данные всегда считаются устаревшими
    refetchOnWindowFocus: true, // Обновляем при фокусе окна
  })

  // Get user's progress data
  const { data: progressData = [], isLoading: progressLoading } = useQuery({
    queryKey: ['allProgress'],
    queryFn: () => getAllTrainingProgress(authData.access_token),
    enabled: authData.access_token !== "",
    staleTime: 2 * 60 * 1000, // 2 минуты
    refetchOnWindowFocus: false,
  })

  const title = {title_top: "Saved trainings:", title_bottom: ""}

  if (isLoading) return <div className="centered-content">
                            <div className="step-title-main">Loading...</div>
                            <p>It may take a while to upload the data</p>
                        </div>                      

  return (
    <>
      {trainingsData.length > 0 ? (
        <CourseCatalogue 
          courses={trainingsData} 
          title={title}
          progressData={progressData}
          savedCourses={trainingsData} // All courses on this page are saved
        />
      ) : (
        <div className="centered-content">
            <div className="step-title-main">Oops...</div>
            <p>You have no saved trainings now, so it's time to explore something new!</p>
            <div className="button-group-welcome">
                <button className="btn-basic-black" onClick={() => navigate("/catalogue")}>Go to Catalogue</button>
            </div>
        </div>
      )}
    </>
  );
};

export default SavedCoursesPage;