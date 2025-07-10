import React, { useEffect } from 'react';
//import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';
import AuthContext from "../components/context/AuthContext";
import { getMyTrainingsRequest, userInfoRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { data, useNavigate } from 'react-router-dom';

const MyCoursesPage = () => {

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
    queryKey: ['myTrainings'],
    queryFn: () => getMyTrainingsRequest(authData.access_token, userData!.id),
    enabled: userData!== null
  })

  

  const title = {title_top: "My trainings:", title_bottom: ""}

  return (
    <>
      <CourseCatalogue courses={trainingsData}/>
    </>
  );
};

export default MyCoursesPage;