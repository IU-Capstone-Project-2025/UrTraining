// import React from 'react'
import Navbar from '../components/Navbar'
import { useQuery } from '@tanstack/react-query';
import { useContext } from 'react';
import AuthContext from '../components/context/AuthContext';
import { userInfoRequest } from '../api/apiRequests';
import type { UserProp } from '../components/interface/userInterface';

const NavbarPage = () => {
    const authData = useContext(AuthContext)

    const { data, isLoading, status } = useQuery({
        queryKey: ['me'],
        queryFn: () => userInfoRequest(authData.access_token),
        enabled: authData.access_token !== ""
    })  

    const userData = data as unknown as UserProp; 

    return (
        <>
            <Navbar {...userData}/>
        </>
    )
}

export default NavbarPage