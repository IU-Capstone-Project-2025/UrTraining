// import React from 'react'
import { useContext } from 'react';
import Welcome from '../components/Welcome';
import AuthContext from '../components/context/AuthContext';

const HomePage = () => {
  const authData = useContext(AuthContext)

  return (
    <>
      <Welcome />
    </>
  )
}

export default HomePage