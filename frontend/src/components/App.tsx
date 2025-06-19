// import React from 'react';
import '../css/App.css';
import './Navbar';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from './Navbar'
import HomePage from '../pages/HomePage';
import SignInPage from '../pages/SignInPage';
import SignUpPage from '../pages/SignUpPage';
import TraineeBeginPage from '../pages/TraineeBeginPage';
import TrainerBeginPage from '../pages/TrainerBeginPage';
import SurveyPage from '../pages/SurveyPage';
import ProfileEditPage from '../pages/ProfileEditPage';
import ProfilePage from '../pages/ProfilePage';
import ExampleCoursePage from '../pages/ExampleCoursePage';
import { AuthProvider, useAuth } from '../context/AuthContext';

// Компонент для защищенных роутов
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Загрузка...</div>;
  }
  
  return isAuthenticated ? <>{children}</> : <Navigate to="/signin" replace />;
};

// Компонент для публичных роутов (только для неавторизованных)
const PublicRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Загрузка...</div>;
  }
  
  return !isAuthenticated ? <>{children}</> : <Navigate to="/" replace />;
};

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navbar />}>
            <Route index element={<HomePage />} />
            <Route path="signup" element={
              <PublicRoute>
                <SignUpPage />
              </PublicRoute>
            } />
            <Route path="signin" element={
              <PublicRoute>
                <SignInPage />
              </PublicRoute>
            } />
            <Route path="trainee-begin" element={
              <ProtectedRoute>
                <TraineeBeginPage />
              </ProtectedRoute>
            } />
            <Route path="trainer-begin" element={
              <ProtectedRoute>
                <TrainerBeginPage />
              </ProtectedRoute>
            } />
            <Route path="survey" element={
              <ProtectedRoute>
                <SurveyPage />
              </ProtectedRoute>
            } />
            <Route path="profile/edit" element={
              <ProtectedRoute>
                <ProfileEditPage />
              </ProtectedRoute>
            } />
            <Route path="profile" element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            } />
            <Route path="course/example-course" element={
              <ProtectedRoute>
                <ExampleCoursePage />
              </ProtectedRoute>
            } />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;


