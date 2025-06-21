// import React from 'react'
import axios, { AxiosError } from 'axios';
import { useContext, useEffect, useState } from "react"
import Sign from "../components/Sign"
import { example_signin_data } from "../components/data/example_json_data"
import type { CredentialsData, SignInSuccess, SignInFailed } from "../components/interface/interfaces"
import SignPageContext, { emptyCredentials, type SignContextType } from "../components/context/SignPageContext"
import { useMutation, useQuery } from "@tanstack/react-query"
import { useNavigate } from 'react-router-dom';
import AuthContext from '../components/context/AuthContext';

const endpoint = 'http://localhost:8000'

async function signInRequest(
  credentials: CredentialsData
): Promise<SignInSuccess> {
  try {
    const resp = await axios.post<SignInSuccess>(
      `${endpoint}/auth/login`,
      credentials
    );
    return resp.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      throw error as AxiosError<SignInFailed>;
    }
    throw error;
  }
}

const SignInPage = () => {
  const [credentials, setCredentials] = useState<CredentialsData>(emptyCredentials)
  const authData = useContext(AuthContext)
  const navigate = useNavigate();


  const contextValue: SignContextType = {
    credentials: credentials,
    sendCredentials: setCredentials
  };

  const signInMutation = useMutation<SignInSuccess, AxiosError<SignInFailed>, CredentialsData>({
    mutationFn: signInRequest,
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token)
      authData.setAccessToken(data.access_token)
      console.log('Logged in!');
      navigate("/")
    },
    onError: (error) => {
      console.error('Login failed:', error);
    },
  });

  useEffect(() => {
    if (credentials !== emptyCredentials) {
      signInMutation.mutate(credentials);
    }
  }, [credentials]);

  return (
    <SignPageContext value={contextValue}>
      <Sign {...example_signin_data} />
    </SignPageContext>
  )
}

export default SignInPage