import React, { useState, useCallback } from 'react'
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

const CourseCatalogue = React.memo(({ courses, title }: CourseCatalogueProps) => {
  const [filteredCourses, setFilteredCourses] = useState<any[]>(() => courses);
  const [showFilters, setShowFilters] = useState<boolean>(false);

  // Обновляем фильтрованные курсы при изменении исходного списка
  React.useEffect(() => {
    setFilteredCourses(courses);
  }, [courses]);

  const handleFilterChange = useCallback((filtered: any[]) => {
    setFilteredCourses(filtered);
  }, []);

  const toggleFilters = useCallback(() => {
    setShowFilters(prev => !prev);
  }, []);
  
  return (
    <div className="catalogue basic-page">

      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
          <filter id="blurOval" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="60" />
          </filter>
      </svg>

      <div className='catalogue__container'>
        <h1 className="catalogue__title">
          <span style={{ display: 'block' }}>{title.title_top}</span>
          <span style={{ display: 'block', marginBottom: '20px', opacity: '20%'}}>{title.title_bottom}</span>
        </h1>

        <div className="catalogue__filter-controls">
          <button 
            onClick={toggleFilters}
            className="catalogue__toggle-filters-btn"
          >
            <span className="catalogue__toggle-filters-icon">
              {showFilters ? '▼' : '▶'}
            </span>
            {showFilters ? 'Hide filtration' : 'Show filtration'}
          </button>
        </div>

        <div className={`catalogue__filters-container ${showFilters ? 'visible' : 'hidden'}`}>
          <TagSearch courses={courses} onFilterChange={handleFilterChange} />
        </div>

        <div className="catalogue__results-count">
          Found {filteredCourses.length} training{filteredCourses.length !== 1 ? 's' : ''}
        </div>

        <div className="catalogue__grid">

          {filteredCourses.map((course: any, index: number) => {
            // Проверяем, что у курса есть корректный ID
            if (!course.id) {
              return null;
            }
            
            return (
              <Link
                to={`/course/${course.id}`} 
                key={course.id}
              >
                <CourseCard {...transformRawCourseData(course)} />
                {(index % 5 == 0) &&
                  <div style={{ position: "relative"}}>
                    <div className="assets__background__gradient" style={{ background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                        filter: 'url(#blurOval)', top: "0", left: "0" }}></div>
                  </div>}
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
});

export default CourseCatalogue