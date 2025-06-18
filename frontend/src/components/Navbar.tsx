import React, { useState } from 'react'
import '../css/Navbar.css'
import { Outlet, Link, useNavigate } from "react-router-dom";
import { authAPI } from '../utils/auth';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { isAuthenticated, userInfo, logout } = useAuth();

  const handleLogout = async () => {
    setLoading(true);
    try {
      await authAPI.logout();
      logout(); // Update context state
      navigate('/');
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setLoading(false);
    }
  };

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
          {isAuthenticated && userInfo ? (
            <>
              <span style={{ 
                marginRight: '15px', 
                color: '#333',
                fontSize: '14px'
              }}>
                Welcome, {userInfo.full_name || userInfo.username}!
              </span>
              <button 
                className='btn-basic-white'
                onClick={handleLogout}
                disabled={loading}
              >
                {loading ? 'Logging out...' : 'Logout'}
              </button>
            </>
          ) : (
            <>
              <button className='btn-basic-white'>
                <Link to="/signin" style={{ textDecoration: 'none', color: 'inherit' }}>
                  Sign In
                </Link>
              </button>
              <button className='btn-basic-black'>
                <Link to="/signup" style={{ textDecoration: 'none', color: 'inherit' }}>
                  Sign Up
                </Link>
              </button>
            </>
          )}
        </div>
      </div>
      <Outlet />
    </>
  )
}

export default Header