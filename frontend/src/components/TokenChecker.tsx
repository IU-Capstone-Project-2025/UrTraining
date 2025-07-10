import React, { useContext, useEffect } from 'react'
import { jwtDecode } from "jwt-decode";
import { useLocation } from 'react-router-dom'
import AuthContext from './context/AuthContext';

export const TokenChecker = () => {
    const authData = useContext(AuthContext)
    const location = useLocation();

    useEffect(() => {

        const checkToken = () => {
            const token = localStorage.getItem('token');
            if (!token && authData.access_token != "") {
                window.location.reload()
                return;
            }
            if (!token) {
                return;
            }
            try {
                const { exp }: { exp: number } = jwtDecode(token);
                if (exp * 1000 < Date.now()) {
                    localStorage.removeItem('token');
                    authData.setAccessToken("");
                } else {
                    authData.setAccessToken(token);
                }
            } catch {
                localStorage.removeItem('token');
                authData.setAccessToken("");
                window.location.reload()
            }
        };

        checkToken();
        const id = setInterval(checkToken, 60 * 1000);
        return () => clearInterval(id);
    }, [location.pathname]);

    return null;
}

export default TokenChecker;