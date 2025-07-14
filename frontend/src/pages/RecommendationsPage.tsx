import React, { useContext, useEffect } from 'react'
import "../css/UploadTrainingPage.css";
import Recommendations from '../components/Recommendations'
import { userInfoRequest, getRecommendations } from '../api/apiRequests';
import AuthContext from '../components/context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
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
    staleTime: 1000 * 60 * 5,
    retry: false
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
      <div className="centered-content basic-page">
        <div className="step-title-main">Oops...</div>
        <p>Please fill the survey to get personalized recommendations. It takes only 2-3 minutes.</p>
        <div className="buttons">
            <button className="btn-basic-black"><Link to={`/survey`}>Go to Survey</Link></button>
            <button className="btn-basic-white"><Link to="/">Main menu</Link></button>
        </div>
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