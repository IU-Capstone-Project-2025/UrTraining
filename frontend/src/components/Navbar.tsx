// import React from 'react'
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Ошибка при выходе:', error);
    }
  };

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
          <Link to="/profile">
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
          {isAuthenticated ? (
            <>
              <span style={{ marginRight: '10px', color: 'black' }}>
                Привет, {user?.full_name || user?.username}!
              </span>
              <button className='btn-basic-white' onClick={handleLogout}>
                Выйти
              </button>
            </>
          ) : (
            <>
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
            </>
          )}
        </div>
      </div>
      <Outlet />
    </>
  )
}

export default Header