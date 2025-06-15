// import React from 'react';
import '../css/App.css';
import './Navbar';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './Navbar'
import HomePage from '../pages/HomePage';
import SignUp from '../pages/SignUpPage';
import SignIn from '../pages/SignInPage';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navbar />}>
          <Route index element={<HomePage />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="signin" element={<SignIn />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;


