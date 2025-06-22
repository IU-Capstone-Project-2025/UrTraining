// import React from 'react'
import { useContext, useEffect, useState } from "react";
import Sign from "../components/Sign"
import { example_signup_data } from "../components/data/example_json_data"
import type { CredentialsData } from "../components/interface/interfaces";
import SignPageContext, { emptyCredentials, type SignContextType } from "../components/context/SignPageContext";
import AuthContext from "../components/context/AuthContext";
import { useSignUp } from "../api/mutations";
import { useNavigate } from "react-router-dom";

const SignUpPage = () => {
  const [credentials, setCredentials] = useState<CredentialsData>(emptyCredentials)
  const authData = useContext(AuthContext)
  const signUpMutation = useSignUp()

  const navigate = useNavigate();

  const contextValue: SignContextType = {
    credentials: credentials,
    sendCredentials: setCredentials
  };

  // If user is already authenticated, 
  // Return to main page
  useEffect(() => {
    if (authData.access_token !== "")
      navigate("/")
  }, [authData])

  // After credentials updated inside <Sign />,
  // call POST Mutation function
  useEffect(() => {
    if (credentials !== emptyCredentials)
      signUpMutation.mutate(credentials)
      navigate("/")
  }, [credentials]);

  return (
    <SignPageContext value={contextValue}>
      <Sign {...example_signup_data} />
    </SignPageContext>
  )
}

export default SignUpPage