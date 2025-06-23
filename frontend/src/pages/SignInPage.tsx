// import React from 'react'
import { useContext, useEffect, useState } from "react"
import Sign from "../components/Sign"
import { example_signin_data } from "../components/data/example_json_data"
import type { CredentialsData } from "../components/interface/interfaces"
import SignPageContext, { emptyCredentials, type SignContextType } from "../components/context/SignPageContext"
import AuthContext from '../components/context/AuthContext';
import { useSignIn } from '../api/mutations';
import { useNavigate } from "react-router-dom"

const SignInPage = () => {
  const [credentials, setCredentials] = useState<CredentialsData>(emptyCredentials)
  const authData = useContext(AuthContext)
  const signInMutation = useSignIn(authData)

  const navigate = useNavigate();

  const contextValue: SignContextType = {
    credentials: credentials,
    submitCredentials: setCredentials
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
    if (credentials !== emptyCredentials) {
      signInMutation.mutate(credentials);
      navigate("/signin")
    }
  }, [credentials]);

  return (
    <SignPageContext value={contextValue}>
      <Sign {...example_signin_data} />
    </SignPageContext>
  )
}

export default SignInPage