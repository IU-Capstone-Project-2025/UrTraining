// import React from 'react'
import { useParams } from 'react-router-dom';
import Course from "../components/Course"
import kanye from '../assets/kanye.jpg'
import { transformRawCourseData } from "../utils/transformRawCouseData"
import { currentTrainingDataRequest } from "../api/apiRequests";
import AuthContext from "../components/context/AuthContext";
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";

const CoursePage = () => {

    const { courseId } = useParams();
    const authData = useContext(AuthContext)

    const { data: courseData = [], isLoading, status } = useQuery<any, Error>({
        queryKey: ['formTraining'],
        queryFn: () => currentTrainingDataRequest(courseId as String, authData.access_token)
    })

    const training_data = transformRawCourseData(courseData);

    return (
        <Course {...training_data} />
    )
}

export default CoursePage