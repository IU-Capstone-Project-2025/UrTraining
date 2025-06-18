// import React from 'react';
import '../css/App.css';
import './Navbar';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './Navbar'
import HomePage from '../pages/HomePage';
import SignInPage from '../pages/SignInPage';
import SignUpPage from '../pages/SignUpPage';
import TraineeBeginPage from '../pages/TraineeBeginPage';
import TrainerBeginPage from '../pages/TrainerBeginPage';
import SurveyPage from '../pages/SurveyPage';
import ProtectedRoute from './ProtectedRoute';
import { AuthProvider } from '../context/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navbar />}>
            <Route index element={<HomePage />} />
            <Route path="signup" element={<SignUpPage />} />
            <Route path="signin" element={<SignInPage />} />
            <Route 
              path="trainee-begin" 
              element={
                <ProtectedRoute>
                  <TraineeBeginPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="trainer-begin" 
              element={
                <ProtectedRoute>
                  <TrainerBeginPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="survey" 
              element={
                <ProtectedRoute>
                  <SurveyPage />
                </ProtectedRoute>
              } 
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;


