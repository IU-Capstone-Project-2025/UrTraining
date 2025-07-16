import React, { useEffect } from 'react';
//import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';
import AuthContext from "../components/context/AuthContext";
import { getMyTrainingsRequest, userInfoRequest } from "../api/apiRequests";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { data, useLocation, useNavigate, useParams } from 'react-router-dom';

const MyCoursesPage = () => {

  const { userId } = useParams();
  const location = useLocation();
  const authorName = location.state?.authorName;
  const authData = useContext(AuthContext);
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
    queryFn: () => getMyTrainingsRequest(authData.access_token, userId as unknown as number),
    enabled: userData!== null
  })

  const title = {title_top: `${authorName}'s training programs:`, title_bottom: `found ${trainingsData.length} trainings`}

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
          progressData={[]} // Other trainer's courses don't need progress tracking
          savedCourses={[]} // Other trainer's courses tracking not relevant here
        />
      ) : (
        <div className="centered-content">
            <div className="step-title-main">Oops...</div>
            <p>This trainer has no created trainings now, but you can view the millions of other trainings!</p>
            <div className="button-group-welcome">
                <button className="btn-basic-black" onClick={() => navigate("/catalogue")}>Go to Catalogue</button>
            </div>
        </div>
      )}
    </>
  );
};

export default MyCoursesPage;