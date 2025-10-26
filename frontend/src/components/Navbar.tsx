// import React from 'react'
import { useContext, useState } from 'react';
import '../css/Navbar.css'
import { Outlet, Link } from "react-router-dom";
import AuthContext from './context/AuthContext';
import type { UserProp } from './interface/userInterface';
import menu from '../assets/Menu.svg'
import arrow from '../assets/arrow.svg'
import { useTranslation } from 'react-i18next';
import LanguageToggleButton from "./LanguageToggleButton";


const Navbar = (data: UserProp) => {
  const authData = useContext(AuthContext)
  const [menuOpen, setMenuOpen] = useState(false);
  const { t, i18n } = useTranslation();

  const changeLang = (lang: 'en' | 'ru') => {
    i18n.changeLanguage(lang);
    localStorage.setItem('lang', lang);
  };

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
            {t('navbar.profile')}
          </Link>
          <Link to={authData.access_token === "" ? "/signin" : "/catalogue"}>
            {t('navbar.catalogue')}
          </Link>
          <Link to={authData.access_token === "" ? "/signin" : "/recommendations"}>
            {t('navbar.recommendations')}
          </Link>
          <Link to={authData.access_token === "" ? "/signin" : "/upload-training"} style={data.trainer_profile === null ? { display: "none" } : {}}
          >
            {t('navbar.upload')}
          </Link>
          <Link to="/about-us">
            {t('navbar.faq')}
          </Link>
        </div>
        <div className='navbar__user'>
          <div
            className='navbar__auth'
            style={authData.access_token !== "" ? { display: "none" } : {}}
          >
            <Link to="/signin">
              <button className='btn-basic-white'>
                {t('navbar.signin')}
              </button>
            </Link>
            <Link to="/signup">
              <button className='btn-basic-black'>
                {t('navbar.signup')}
              </button>
            </Link>
          </div>
          <div
            className='navbar__user__data'
            style={authData.access_token === "" ? { display: "none" } : {}}
          >
            <Link to={authData.access_token === "" ? "/signin" : "/profile"}><h2>{t('navbar.hello')}, {data?.username ?? "none"}</h2></Link>
          </div>
          <LanguageToggleButton />
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
                {t('navbar.signin')}
              </button>
            </Link>
            <Link to="/signup" onClick={() => setMenuOpen(!menuOpen)}>
              <button className='btn-basic-black'>
                {t('navbar.signup')}
              </button>
            </Link>
          </div>
          <div
            className='navbar__user__data'
            style={authData.access_token === "" ? { display: "none" } : {}}
          >
            <h2>{t('navbar.hello')}, {data?.username ?? "none"}</h2>
          </div>

          <div className='navbar__links navbar__mobile'>
            <Link to={authData.access_token === "" ? "/signin" : "/profile"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>{t('navbar.profile')}</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to={authData.access_token === "" ? "/signin" : "/catalogue"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>{t('navbar.catalogue')}</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to={authData.access_token === "" ? "/signin" : "/recommendations"} onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>{t('navbar.recommendations')}</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to={authData.access_token === "" ? "/signin" : "/upload-training"} 
                  style={data.trainer_profile === null ? { display: "none" } : {}} 
                  onClick={() => setMenuOpen(!menuOpen)}
            >
              <div className='navbar__mobile__link'>
                <h3>{t('navbar.upload')}</h3>
                <img src={arrow} alt="" />
              </div>
            </Link>
            <Link to="/about-us" onClick={() => setMenuOpen(!menuOpen)}>
              <div className='navbar__mobile__link'>
                <h3>{t('navbar.faq')}</h3>
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