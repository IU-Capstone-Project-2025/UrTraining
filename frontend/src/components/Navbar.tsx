// import React from 'react'
import '../css/Navbar.css'

const Header = () => {
  return (
    <div className='navbar'>
        <div className='navbar__logo'>
            <h1>URTRAINING</h1>
        </div>
        <div className='navbar__links'>
            <h3>Profile</h3>
            <h3>Catalogue</h3>
            <h3>Recommendations</h3>
            <h3>Upload</h3>
            <h3>About Us</h3>
        </div>
        <div className='navbar__auth'>
            <h3>Sign In</h3>
            <h3>Sign Up</h3>
        </div>
    </div>
  )
}

export default Header