// import React from 'react'
import { useParams } from 'react-router-dom';
import Course from "../components/Course"
import kanye from '../assets/kanye.jpg'
import { transformRawCourseData } from "../utils/transformRawCouseData"
import courses from "../components/data/selected_courses_with_ids_plus_plan.json"

const CoursePage = () => {

    const { courseId } = useParams();

    const courseData = courses.find(course => course.id === courseId);
    const training_data = transformRawCourseData(courseData);

    return (
        <Course {...training_data} />
    )
}

export default CoursePage