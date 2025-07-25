// import React from 'react'
import { useContext, useEffect, useState } from "react"
import Sign from "../components/Sign"
import { example_signin_data } from "../components/data/example_json_data"
import type { CredentialsData } from "../components/interface/interfaces"
import SignPageContext, { emptyCredentials, type SignContextType } from "../components/context/SignPageContext"
import AuthContext from '../components/context/AuthContext';
import { useSignIn } from '../api/mutations';
import { useNavigate } from "react-router-dom"
import type { Axios, AxiosError } from "axios"

const SignInPage = () => {
  const [credentials, setCredentials] = useState<CredentialsData>(emptyCredentials)
  const [isError, setIsError] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")
  const authData = useContext(AuthContext)
  const signInMutation = useSignIn()

  const navigate = useNavigate();

  const contextValue: SignContextType = {
    credentials: credentials,
    isError: isError,
    errorMessage: errorMessage,
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
      signInMutation.mutate(credentials, {
        onSuccess: (data) => {
          setIsError(false)
          localStorage.setItem("token", data.access_token);
          authData.setAccessToken(data.access_token);
          console.log("Logged in!");
        },
        onError: (error: any) => {
          setIsError(true)
          setErrorMessage(error.response?.data?.detail[0].msg || error.response?.data?.detail)
          console.error("Login failed: ", error);
        }
      });
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