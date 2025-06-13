// import React from 'react'
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";

const Header = () => {
  return (
    <>
      <div className='navbar'>
        <div className='navbar__logo'>
          <Link to="/">
            <h1>URTRAINING</h1>
          </Link>
        </div>
        <div className='navbar__links'>
          <h3>Profile</h3>
          <h3>Catalogue</h3>
          <h3>Recommendations</h3>
          <h3>Upload</h3>
          <h3>About Us</h3>
        </div>
        <div className='navbar__auth'>
          <button className='btn-basic-white' style={{ padding: "4px 20px" }}>
            <Link to="/signup">
              Sign In
            </Link>
          </button>
          <button className='btn-basic-black' style={{ padding: "4px 20px" }}>
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