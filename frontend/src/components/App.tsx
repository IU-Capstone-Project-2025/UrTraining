// import React from 'react';
import '../css/App.css';
import './Navbar';
import { jwtDecode } from "jwt-decode";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import NavbarPage from '../pages/NavbarPage';
import HomePage from '../pages/HomePage';
import SignInPage from '../pages/SignInPage';
import SignUpPage from '../pages/SignUpPage';
import TraineeBeginPage from '../pages/TraineeBeginPage';
import TrainerBeginPage from '../pages/TrainerBeginPage';
import SurveyPage from '../pages/SurveyPage';
import ExampleCoursePage from '../pages/ExampleCoursePage';
import { useEffect, useState } from 'react';
import { AuthContext, type AuthCredentialsTokens } from './context/AuthContext';
import axios from 'axios';

const queryClient = new QueryClient()

const App = () => {
  const [accessToken, SetAccessToken] = useState<String>("")

  useEffect(() => {
    // It is necessary to use accessToken in any
    // API Request because in this function should
    // happen any check of validity of specified token.
    const token = localStorage.getItem('token')

    // Check if token exist
    if (token) {
      const { exp } = jwtDecode(token)

      console.log(exp);

      // Check in expiry is defined
      if (exp)
        // Remove token if expired
        if (exp * 1000 < Date.now())
          localStorage.removeItem('token');

      // Set as access token otherwise
      SetAccessToken(token)
    }
  })

  const contextValue: AuthCredentialsTokens = {
    access_token: accessToken,
    setAccessToken: SetAccessToken
  }

  return (
    <AuthContext value={contextValue}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<NavbarPage />}>
              <Route index element={<HomePage />} />
              <Route path="signup" element={<SignUpPage />} />
              <Route path="signin" element={<SignInPage />} />
              <Route path="trainee-begin" element={<TraineeBeginPage />} />
              <Route path="trainer-begin" element={<TrainerBeginPage />} />
              <Route path="survey" element={<SurveyPage />} />
              <Route path="course/example-course" element={<ExampleCoursePage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </AuthContext>
  );
};

export default App;


