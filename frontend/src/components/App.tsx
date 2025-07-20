// import React from 'react';
import '../css/App.css';
import './Navbar';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import TokenChecker from './TokenChecker';
import NavbarPage from '../pages/NavbarPage';
import HomePage from '../pages/HomePage';
import SignInPage from '../pages/SignInPage';
import SignUpPage from '../pages/SignUpPage';
import TraineeBeginPage from '../pages/TraineeBeginPage';
import TrainerBeginPage from '../pages/TrainerBeginPage';
import AboutUsPage from '../pages/AboutUsPage';
import SurveyPage from '../pages/SurveyPage';
import AdvancedRegistrationPage from '../pages/AdvancedRegistrationPage';
import CoursesCataloguePage from '../pages/CoursesCataloguePage';
import CoursePage from '../pages/CoursePage';
import { useEffect, useState } from 'react';
import { AuthContext, type AuthCredentialsTokens } from './context/AuthContext';
import RecommendationsPage from '../pages/RecommendationsPage';
import UploadTrainingPage from '../pages/UploadTrainingPage';
import ProfilePage from '../pages/ProfilePage';
import MyCoursesPage from '../pages/MyCoursesPage';
import AIUploadPage from '../pages/AIUploadPage';
import MetadataContext from './context/MetadataContext';
import SavedCoursesPage from '../pages/SavedCoursesPage';
import CurrentTrainerCoursesPage from '../pages/CurrentTrainerCoursesPage';
import TrainingsByDatePage from '../pages/TrainingsByDatePage';

const queryClient = new QueryClient()

const App = () => {
  const [accessToken, SetAccessToken] = useState<String>("")

  const contextValue: AuthCredentialsTokens = {
    access_token: accessToken,
    setAccessToken: SetAccessToken
  }

  const metadataContextValue: any = {
    access_token: "",
    setAccessToken: () => { }
  }

  return (

    <AuthContext value={contextValue}>
      <MetadataContext value={metadataContextValue}>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>

            <svg style={{ position: 'absolute', width: 0, height: 0 }}>
              <defs>
                <filter
                  id="blurOval"
                  x="-50%" y="-50%" width="200%" height="200%"
                  colorInterpolationFilters="sRGB"
                >
                  <feGaussianBlur in="SourceGraphic" stdDeviation="60" />
                </filter>
              </defs>
            </svg>

            <TokenChecker />
            <Routes>
              <Route path="/" element={<NavbarPage />}>
                <Route index element={<HomePage />} />
                <Route path="signup" element={<SignUpPage />} />
                <Route path="signin" element={<SignInPage />} />
                <Route path="trainee-begin" element={<TraineeBeginPage />} />
                <Route path="trainer-begin" element={<TrainerBeginPage />} />
                <Route path="about-us" element={<AboutUsPage />} />
                <Route path="survey" element={<SurveyPage />} />
                <Route path="trainer-registration" element={<AdvancedRegistrationPage />} />
                <Route path="catalogue" element={<CoursesCataloguePage />} />
                <Route path="my-trainings" element={<MyCoursesPage />} />
                <Route path="saved-trainings" element={<SavedCoursesPage />} />
                <Route path="recommendations" element={<RecommendationsPage />} />
                <Route path="course/:courseId" element={<CoursePage />} />
                <Route path="catalogue/:userId" element={<CurrentTrainerCoursesPage />} />
                <Route path="upload-training" element={<UploadTrainingPage />} />
                <Route path="ai-upload" element={<AIUploadPage />} />
                <Route path="profile" element={<ProfilePage />} />
                <Route path="calendar/:currentDate" element={<TrainingsByDatePage />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </QueryClientProvider>
      </MetadataContext>
    </AuthContext>
  );
};

export default App;


