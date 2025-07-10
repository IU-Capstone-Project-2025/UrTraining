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
import SurveyPage from '../pages/SurveyPage';
import AdvancedRegistrationPage from '../pages/AdvancedRegistrationPage';
import CoursesCataloguePage from '../pages/CoursesCataloguePage';
import CoursePage from '../pages/CoursePage';
import { useEffect, useState } from 'react';
import { AuthContext, type AuthCredentialsTokens } from './context/AuthContext';
import RecommendationsPage from '../pages/RecommendationsPage';
import UploadTrainingPage from '../pages/UploadTrainingPage';
import ProfilePage from '../pages/ProfilePage';
import AIUploadPage from '../pages/AIUploadPage';
import MetadataContext from './context/MetadataContext';

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
            <TokenChecker />
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
                <Route path="course/:courseId" element={<CoursePage />} />

                <Route path="upload-training" element={<UploadTrainingPage />} />
                <Route path="ai-upload" element={<AIUploadPage />} />
                <Route path="profile" element={<ProfilePage />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </QueryClientProvider>
      </MetadataContext>
    </AuthContext>
  );
};

export default App;


