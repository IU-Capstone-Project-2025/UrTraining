// import React from 'react'
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";

const Header = () => {
  return (
    <>
      <div className='navbar'>
        <div className='navbar__logo'>
          <Link to="/">
            <h1>
              URTRAINING
            </h1>
          </Link>
        </div>
        <div className='navbar__links'>
          <Link to="/">
            Profile
          </Link>
          <Link to="/">
            Catalogue
          </Link>
          <Link to="/">
            Recommendations
          </Link>
          <Link to="/">
            Upload
          </Link>
          <Link to="/">
            About Us
          </Link>
        </div>
        <div className='navbar__auth'>
          <button className='btn-basic-white'>
            <Link to="/signup">
              Sign In
            </Link>
          </button>
          <button className='btn-basic-black'>
            <Link to="/signup">
              Sign Up
            </Link>
          </button>
        </div>
      </div>
      <Outlet />
    </>
  )
}

export default Header