// import React from 'react'
import { useContext } from 'react';
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";
import AuthContext from './context/AuthContext';
import type { UserProp } from './interface/userInterface';

const Navbar = (data: UserProp) => {
  const authData = useContext(AuthContext)

  return (
    <>
      <div className='navbar'>
        <Link to="/">
          <div className='navbar__logo'>
            <h1>
              URTRAINING
            </h1>
          </div>
        </Link>
        <div className='navbar__links'>
          <Link to={authData.access_token === "" ? "/signin" : "/profile"}>
            Profile
          </Link>
          <Link to={authData.access_token === "" ? "/signin" : "/catalogue"}>
            Catalogue
          </Link>
          <Link to={authData.access_token === "" ? "/signin" : "/recommendations"}>
            Recommendations
          </Link>
          <Link to={authData.access_token === "" ? "/signin" : "/upload-training"}>
            Upload
          </Link>
          <Link to="http://t.me/mescudiway">
            About Us
          </Link>
        </div>
        <div className='navbar__user'>
          <div
            className='navbar__auth'
            style={authData.access_token !== "" ? { display: "none" } : {}}
          >
            <Link to="/signin">
              <button className='btn-basic-white'>
                Sign In
              </button>
            </Link>
            <Link to="/signup">
              <button className='btn-basic-black'>
                Sign Up
              </button>
            </Link>
          </div>
          <div
            className='navbar__user__data'
            style={authData.access_token === "" ? { display: "none" } : {}}
          >
            <h2>Hello, {data?.username ?? "none"}</h2>
          </div>
        </div>
      </div>
      <Outlet />
    </>
  )
}

export default Navbar