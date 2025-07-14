// import React from 'react'
import { useContext, useEffect, useState } from "react";
import Sign from "../components/Sign"
import { example_signup_data } from "../components/data/example_json_data"
import type { CredentialsData } from "../components/interface/interfaces";
import SignPageContext, { emptyCredentials, type SignContextType } from "../components/context/SignPageContext";
import AuthContext from "../components/context/AuthContext";
import { useSignUp, useSignIn } from "../api/mutations";
import { useNavigate, useSearchParams } from "react-router-dom";
import type { AxiosError } from "axios";

const SignUpPage = () => {
  const [credentials, setCredentials] = useState<CredentialsData>(emptyCredentials)
  const [isError, setIsError] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")
  const authData = useContext(AuthContext)
  const signUpMutation = useSignUp()
  const signInMutation = useSignIn()

  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const role = searchParams.get("role");

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
      if (role === "trainer") {
            navigate("/trainer-registration");
          } else if (role === "trainee") {
            navigate("/survey");
          } else {
            navigate("/"); // fallback
          }
  }, [authData])

  // After credentials updated inside <Sign />,
  // call POST Mutation function
  useEffect(() => {
    if (credentials !== emptyCredentials) {
      signUpMutation.mutate(credentials, {
        onSuccess: (data) => {
          setIsError(false)
          console.log("Signup succeeded on this call:", data);

          localStorage.setItem("token", data.access_token);
          authData.setAccessToken(data.access_token);

          console.log(role)
          
          if (role === "trainer") {
            navigate("/trainer-registration");
          } else if (role === "trainee") {
            navigate("/survey");
          } else {
            navigate("/"); // fallback
          }
        },
        onError: (error: any) => {
          setIsError(true)
          setErrorMessage(error.response?.data?.detail[0].msg || error.response?.data?.detail)  
          console.error("Signup failed on this call:", error);
        }
      });
    }
  }, [credentials]);

  return (
    <SignPageContext value={contextValue}>
      <Sign {...example_signup_data} />
    </SignPageContext>
  )
}

export default SignUpPage