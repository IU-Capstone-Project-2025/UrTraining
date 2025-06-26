import React from 'react';
//import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';
import AuthContext from "../components/context/AuthContext";
import { trainingsDataRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";

const CoursesCataloguePage = () => {

  const authData = useContext(AuthContext)

  const { data: trainingsData = [], isLoading, status } = useQuery<any, Error>({
    queryKey: ['formTrainings'],
    queryFn: () => trainingsDataRequest(authData.access_token)
  })

  return (
    <>
      <CourseCatalogue courses={trainingsData}/>
    </>
  );
};

export default CoursesCataloguePage;