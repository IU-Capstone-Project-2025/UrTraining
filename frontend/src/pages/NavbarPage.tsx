// import React from 'react'
import Navbar from '../components/Navbar'
import { useQuery } from '@tanstack/react-query';
import { useContext } from 'react';
import AuthContext from '../components/context/AuthContext';
import { userInfoRequest } from '../api/apiRequests';

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