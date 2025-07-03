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
import AdvancedRegistrationPage from '../pages/AdvancedRegistrationPage';
import CoursesCataloguePage from '../pages/CoursesCataloguePage';
import ExampleCoursePage from '../pages/ExampleCoursePage';
import CoursePage from '../pages/CoursePage';
import { useEffect, useState } from 'react';
import { AuthContext, type AuthCredentialsTokens } from './context/AuthContext';
import RecommendationsPage from '../pages/RecommendationsPage';
import UploadTrainingPage from '../pages/UploadTrainingPage';
import ProfilePage from '../pages/ProfilePage';

const queryClient = new QueryClient()

const App = () => {
  const [accessToken, SetAccessToken] = useState<String>("")

  useEffect(() => {
    const checkToken = () => {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }
      try {
        const { exp }: { exp: number } = jwtDecode(token);
        if (exp * 1000 < Date.now()) {
          localStorage.removeItem('token');
          SetAccessToken("");
        } else {
          SetAccessToken(token);
        }
      } catch {
        localStorage.removeItem('token');
        SetAccessToken("");
      }
    };

    checkToken();
    const id = setInterval(checkToken, 60 * 1000);
    return () => clearInterval(id);
  }, []);

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
              <Route path="trainer-registration" element={<AdvancedRegistrationPage />} />
              <Route path="catalogue" element={<CoursesCataloguePage />} />
              <Route path="recommendations" element={<RecommendationsPage />} />
              <Route path="course/example-course" element={<ExampleCoursePage />} />
              <Route path="course/:courseId" element={<CoursePage />} />
              <Route path="upload-training" element={<UploadTrainingPage />} />
              <Route path="profile" element={<ProfilePage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </AuthContext>
  );
};

export default App;


