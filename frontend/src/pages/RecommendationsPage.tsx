import React from 'react'
import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import Recommendations from '../components/Recommendations'

const RecommendationsPage = () => {
  return (
    <>
        <Recommendations courses={courses}/>
    </>
  )
}

export default RecommendationsPage