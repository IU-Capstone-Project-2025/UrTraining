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
import { useTranslation } from 'react-i18next';

const MyCoursesPage = () => {

  const authData = useContext(AuthContext)
  const navigate = useNavigate();
  const { t } = useTranslation();

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

  const title = {title_top: t("catalogue.my"), title_bottom: ""}

  if (isLoading) return <div className="centered-content">
                            <div className="step-title-main">{t("catalogue.loading")}</div>
                            <p>{t("catalogue.load_desc")}</p>
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
            <div className="step-title-main">{t("catalogue.oops")}</div>
            <p>{t("catalogue.no_uploaded")}</p>
            <div className="button-group-welcome">
                <button className="btn-basic-black" onClick={() => navigate("/upload-training")}>{t("catalogue.upload")}</button>
            </div>
        </div>
      )}
    </>
  );
};

export default MyCoursesPage;