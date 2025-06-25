import React from 'react';
import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCatalogue from '../components/CourseCatalogue';

const CoursesCataloguePage = () => {
  const catalogCourses = courses.map(course => {
    const transformed = transformRawCourseData(course);
    return {
      id: course.id,
      title: transformed.course_info.title,
      author: transformed.course_info.author,
      tags: transformed.header_badges.training_type.map(t => t.badge_text),
      rating: transformed.course_info.rating,
      reviews: transformed.course_info.reviews
    };
  });

  return (
    <>
      <CourseCatalogue courses={courses}/>
    </>
  );
};

export default CoursesCataloguePage;