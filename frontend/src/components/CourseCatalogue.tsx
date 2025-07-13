import React, { useState } from 'react'
import CourseCard from './CourseCard';
import TagSearch from './TagSearch';
import "../css/CoursesCatalogue.css";
import { Link } from 'react-router-dom';
import { transformRawCourseData } from '../utils/transformRawCouseData';

type CourseCatalogueProps = {
  courses: any[];
  title: {
    title_top: string;
    title_bottom: string;
  };
};

const CourseCatalogue = ({ courses, title }: CourseCatalogueProps) => {
  const [filteredCourses, setFilteredCourses] = useState<any[]>(courses);

  // Обновляем фильтрованные курсы при изменении исходного списка
  React.useEffect(() => {
    setFilteredCourses(courses);
  }, [courses]);

  const handleFilterChange = (filtered: any[]) => {
    setFilteredCourses(filtered);
  };
  
  return (
    <div className="catalogue basic-page">
      <div className='catalogue__container'>
        <h1 className="catalogue__title">
          <span style={{ display: 'block' }}>{title.title_top}</span>
          <span style={{ display: 'block', marginBottom: '20px', opacity: '20%'}}>{title.title_bottom}</span>
        </h1>

        <TagSearch courses={courses} onFilterChange={handleFilterChange} />

        <div className="catalogue__results-count">
          Found {filteredCourses.length} training{filteredCourses.length !== 1 ? 's' : ''}
        </div>

        <div className="catalogue__grid">

          {filteredCourses.map((course: any, index: number) => (
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