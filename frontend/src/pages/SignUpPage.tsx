// import React from 'react'
import { example_signup_data } from "../components/data/example_json_data"
import Sign from "../components/Sign"

const SignUpPage = () => {
  
  return (
    <>
      <Sign {...example_signup_data} />
    </>
  )
}

export default SignUpPage