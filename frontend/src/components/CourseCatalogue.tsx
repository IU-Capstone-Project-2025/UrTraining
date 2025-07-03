import React from 'react'
import CourseCard from './CourseCard';
import "../css/CoursesCatalogue.css";
import { Link } from 'react-router-dom';
import { transformRawCourseData } from '../utils/transformRawCouseData';

const CourseCatalogue = (data: any) => {
  return (
    <div className="catalogue basic-page">
      <div className='catalogue__container'>
        <h1 className="catalogue__title">
          <span style={{ display: 'block' }}>All trainings</span>
          <span style={{ display: 'block' }}>in one place</span>
        </h1>

        <div className="catalogue__grid">

          {data.courses.map((course: any, index: number) => (
            <Link
              to={`/course/${course.id}`} key={course.id}
            >
              <CourseCard {...transformRawCourseData(course)} />
              {(index % 5 == 0) &&
                <div style={{ position: "relative" }}>
                  <div className="assets__background__gradient" style={{ top: "0", left: "0" }}></div>
                </div>}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CourseCatalogue