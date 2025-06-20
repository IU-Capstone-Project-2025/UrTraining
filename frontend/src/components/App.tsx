// import React from 'react';
import '../css/App.css';
import './Navbar';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Navbar from './Navbar'
import HomePage from '../pages/HomePage';
import SignInPage from '../pages/SignInPage';
import SignUpPage from '../pages/SignUpPage';
import TraineeBeginPage from '../pages/TraineeBeginPage';
import TrainerBeginPage from '../pages/TrainerBeginPage';
import SurveyPage from '../pages/SurveyPage';
import ExampleCoursePage from '../pages/ExampleCoursePage';

const queryClient = new QueryClient()

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navbar />}>
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
  );
};

export default App;


