import React, { useContext, useEffect } from 'react'
import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import Recommendations from '../components/Recommendations'
import { userInfoRequest } from '../api/apiRequests';
import AuthContext from '../components/context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';

const RecommendationsPage = () => {

  const authData = useContext(AuthContext)
  const navigate = useNavigate();

  // vvvvvvvvvvvv
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // PLEASE FIX!!!
  // vvvvvvvvvvvv

  const { data: userData, isLoading: userDataIsLoading, status: userDataStatus } = useQuery({
    queryKey: ['me'],
    queryFn: () => userInfoRequest(authData.access_token),
    enabled: authData.access_token !== ""
  })

  useEffect(() => {
    if (userData === undefined)
      navigate("/signin")
  })

  return (
    <>
        <Recommendations courses={courses}/>
    </>
  )
}

export default RecommendationsPage