import React, { useEffect } from 'react';
//import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';
import AuthContext from "../components/context/AuthContext";
import { trainingsDataRequest, userInfoRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { data, useNavigate } from 'react-router-dom';

const CoursesCataloguePage = () => {

  const authData = useContext(AuthContext)
  const navigate = useNavigate();

  const { data: trainingsData = [], isLoading, status } = useQuery<any, Error>({
    queryKey: ['formTrainings'],
    queryFn: () => trainingsDataRequest(authData.access_token)
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
    enabled: authData.access_token !== ""
  })

  useEffect(() => {
    if (userData === undefined)
      navigate("/signin")
  })

  const title = {title_top: "All trainings", title_bottom: "in one place"}

  return (
    <>
      <CourseCatalogue courses={trainingsData} title={title} />
    </>
  );
};

export default CoursesCataloguePage;