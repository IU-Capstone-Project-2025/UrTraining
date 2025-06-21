// import React from 'react'
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";

const Header = () => {
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
      </div>
      <Outlet />
    </>
  )
}

export default Header