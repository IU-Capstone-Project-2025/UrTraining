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
  progressData?: any[];
  savedCourses?: any[];
};

const CourseCatalogue = React.memo(({ courses, title, progressData = [], savedCourses = [] }: CourseCatalogueProps) => {
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
            
            // Find progress for this course
            const courseProgress = progressData.find((progress: any) => progress.course_id === course.id);
            
            // Check if course is saved
            const isSaved = savedCourses.some((savedCourse: any) => savedCourse.id === course.id);
            
            // If course is saved but no progress record exists, show 0%
            const progressPercentage = isSaved 
              ? (courseProgress?.progress_percentage ?? 0) 
              : courseProgress?.progress_percentage;
            
            return (
              <Link
                to={`/course/${course.id}`} 
                key={course.id}
              >
                <CourseCard 
                  {...transformRawCourseData(course)} 
                  progressPercentage={progressPercentage}
                  isSaved={isSaved}
                />
                {(index % 5 == 0) &&
                  <div style={{ position: "relative" }}>
                    <svg
                        width="1200"
                        height="1200"
                        viewBox="0 0 1200 1200"
                        style={{
                            position: "absolute",
                            top: "-400px",
                            right: "-500px",
                            zIndex: -1,
                            pointerEvents: "none"
                        }}
                        >
                        <defs>
                            <filter
                            id="blurOval"
                            x="-50%"
                            y="-50%"
                            width="200%"
                            height="200%"
                            filterUnits="objectBoundingBox"
                            >
                            <feGaussianBlur in="SourceGraphic" stdDeviation="80" />
                            </filter>

                            <linearGradient id="grad" x1="0%" y1="100%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                            <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                            </linearGradient>
                        </defs>

                        <ellipse
                            cx="600"
                            cy="600"
                            rx="300"
                            ry="200"
                            fill="url(#grad)"
                            filter="url(#blurOval)"
                        />
                    </svg>
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