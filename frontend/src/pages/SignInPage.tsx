// import React from 'react'
import Sign from "../components/Sign"
import { example_signin_data } from "../components/data/example_json_data"

const SignInPage = () => {
  
  return (
    <>
      <Sign {...example_signin_data}/>
    </>
  )
}

export default SignInPage