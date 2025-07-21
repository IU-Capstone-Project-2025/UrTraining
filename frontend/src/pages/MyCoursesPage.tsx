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
          progressData={[]} // My own courses don't need progress tracking
          savedCourses={[]} // My own courses are not "saved" by me
        />
      ) : (
        <div className="centered-content">
            <div className="step-title-main">Oops...</div>
            <p>You have no created trainings now, but you can upload new training plan with our tools!</p>
            <div className="button-group-welcome">
                <button className="btn-basic-black" onClick={() => navigate("/upload-training")}>Upload training</button>
            </div>
        </div>
      )}
    </>
  );
};

export default MyCoursesPage;