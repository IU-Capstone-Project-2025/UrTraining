// import React from 'react'
import axios, { AxiosError } from "axios";
import { useEffect, useState } from "react";
import Sign from "../components/Sign"
import { example_signup_data } from "../components/data/example_json_data"
import type { CredentialsData, SignUpFailed, SignUpSuccess } from "../components/interface/interfaces";
import SignPageContext, { emptyCredentials, type SignContextType } from "../components/context/SignPageContext";
import { useMutation } from "@tanstack/react-query";

const endpoint = 'http://localhost:8000'

async function signUpRequest(
  credentials: CredentialsData
): Promise<SignUpSuccess> {
  try {
    const resp = await axios.post<SignUpSuccess>(
      `${endpoint}/auth/register`,
      credentials
    );
    return resp.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      throw error as AxiosError<SignUpFailed>;
    }
    throw error;
  }
}

const SignUpPage = () => {
  const [credentials, setCredentials] = useState<CredentialsData>(emptyCredentials)

  const contextValue: SignContextType = {
    credentials: credentials,
    sendCredentials: setCredentials
  };

  const signUpMutation = useMutation<SignUpSuccess, AxiosError<SignUpFailed>, CredentialsData>({
      mutationFn: signUpRequest,
      onSuccess: (data) => {
        console.log('Register success:', data.message);
      },
      onError: (error) => {
        console.error('Register failed:', error);
      },
    });

  useEffect(() => {
      if (credentials !== emptyCredentials) {
        console.log(credentials);
        signUpMutation.mutate(credentials)
      }
    }, [credentials]);

  return (
    <SignPageContext value={contextValue}>
      <Sign {...example_signup_data} />
    </SignPageContext>
  )
}

export default SignUpPage