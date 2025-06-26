import React from 'react'
import CourseCard from './CourseCard'
import { data, Link } from 'react-router-dom'
import { transformRawCourseData } from '../utils/transformRawCouseData'

const Recommendations = (data: any) => {
    return (
        <div className="catalogue basic-page">
            <div className='catalogue__container'>
                <h1 className="catalogue__title">
                    <span style={{ display: 'block' }}>Recommended courses</span>
                    <span style={{ display: 'block' }}>Specifically for you</span>
                </h1>

                <div className="catalogue__grid">

                    {data.courses.map((course: any) => (
                        <Link
                            to={`/course/${course.id}`} key={course.id}
                        >
                            <CourseCard {...transformRawCourseData(course)} />
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default Recommendations