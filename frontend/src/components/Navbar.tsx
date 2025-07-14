// import React from 'react'
import { useContext, useState } from 'react';
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";
import AuthContext from './context/AuthContext';
import type { UserProp } from './interface/userInterface';
import menu from '../assets/Menu.svg'
import arrow from '../assets/arrow.svg'

const Navbar = (data: UserProp) => {
  const authData = useContext(AuthContext)
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      <div className='navbar'>
        <div className='navbar__menu'></div>
        <Link to="/" className='navbar__logo' onClick={() => setMenuOpen(false)}>
          <h1>
            URTRAINING
          </h1>
        </Link>
        <div className='navbar__menu'>
          <img src={menu} alt="" onClick={() => setMenuOpen(!menuOpen)} />
        </div>
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
          <Link to="/about-us">
            FAQ
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

      {menuOpen && (
        <div className='navbar__mobile__container'>
          <div
            className='navbar__auth'
            style={authData.access_token !== "" ? { display: "none" } : {}}
          >
            <Link to="/signin" onClick={() => setMenuOpen(!menuOpen)}>
              <button className='btn-basic-white'>
                Sign In
              </button>
            </Link>
            <Link to="/signup" onClick={() => setMenuOpen(!menuOpen)}>
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

          <div className='navbar__links navbar__mobile'>
            <Link to={authData.access_token === "" ? "/signin" : "/profile"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>Profile</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to={authData.access_token === "" ? "/signin" : "/catalogue"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>Catalogue</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to={authData.access_token === "" ? "/signin" : "/recommendations"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>Recommendations</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to={authData.access_token === "" ? "/signin" : "/upload-training"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>Upload</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to="http://t.me/mescudiway" onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>About Us</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
          </div>
        </div>
      )}
      <Outlet />
    </>
  )
}

export default Navbar