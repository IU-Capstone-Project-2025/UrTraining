import React from 'react';
import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import { transformRawCourseData } from '../utils/transformRawCouseData';
import '../css/CoursesCatalogue.css';
import CourseCard from "../components/CourseCard";

const CoursesCatalogue: React.FC = () => {
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
    <div className="catalog-container">
      <h1 className="catalog-title">
        <span style={{display: 'block'}}>All trainings</span>
        <span style={{display: 'block'}}>in one place</span>
      </h1>

      <div className="course-grid">
        {courses.map((course) => (
          <CourseCard key={course.id} {...transformRawCourseData(course)} />
        ))}
      </div>
    </div>
  );
};

export default CoursesCatalogue;