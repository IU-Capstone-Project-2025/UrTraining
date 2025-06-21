// import React from 'react'
import axios, { AxiosError } from 'axios';
import Navbar from '../components/Navbar'
import type { SignInFailed } from '../components/interface/interfaces';
import { useQuery } from '@tanstack/react-query';
import { useContext } from 'react';
import AuthContext from '../components/context/AuthContext';
import type { UserProp } from '../components/interface/userInterface';

const endpoint = 'http://localhost:8000'

async function userInfoRequest(
    token: String
): Promise<String> {
  try {
    const resp = await axios.get<String>(
      `${endpoint}/auth/me`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    return resp.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      throw error as AxiosError<SignInFailed>;
    }
    throw error;
  }
}

const NavbarPage = () => {
    const authData = useContext(AuthContext)

    const { data, isLoading, status } = useQuery({
        queryKey: ['me'],
        queryFn: () => userInfoRequest(authData.access_token),
        enabled: authData.access_token !== ""
    })  

    return (
        <>
            <Navbar {...data}/>
        </>
    )
}

export default NavbarPage