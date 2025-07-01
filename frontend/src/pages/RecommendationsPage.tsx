import React, { useContext, useEffect } from 'react'
import courses from '../components/data/selected_courses_with_ids_plus_plan.json';
import Recommendations from '../components/Recommendations'
import { userInfoRequest, getRecommendations } from '../api/apiRequests';
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

  const {
    data: recommendations,
    isLoading: recsIsLoading,
    error: recsError
  } = useQuery({
    queryKey: ['recommendations', userData?.id],
    queryFn: () => getRecommendations(authData.access_token),
    enabled: !!userData?.id && !!authData.access_token,
    staleTime: 1000 * 60 * 5
  });

  useEffect(() => {
    if (userData === undefined)
      navigate("/signin")
  })

  if (userDataIsLoading || recsIsLoading) {
    return <div className="loading-spinner">Recommendation loading...</div>;
  }

  if (recsError) {
    return (
      <div className="error-message">
        Error when receiving recommendations. Retry later.
      </div>
    );
  }

  return (
    <>
        <Recommendations courses={recommendations}/>
    </>
  )
}

export default RecommendationsPage