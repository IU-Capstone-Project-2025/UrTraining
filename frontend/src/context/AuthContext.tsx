import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { tokenUtils, userUtils } from '../utils/auth';
import type { UserInfo } from '../utils/auth';

interface AuthContextType {
    isAuthenticated: boolean;
    userInfo: UserInfo | null;
    isLoading: boolean;
    login: (token: string, userInfo: UserInfo) => void;
    logout: () => void;
    updateUserInfo: (userInfo: UserInfo) => void;
    refreshAuth: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    const checkAuthStatus = () => {
        try {
            console.log('AuthContext: Checking authentication status...');
            const token = tokenUtils.getToken();
            console.log('AuthContext: Token found:', !!token);
            console.log('AuthContext: Token value (first 20 chars):', token?.substring(0, 20));
            
            const authenticated = tokenUtils.isAuthenticated();
            console.log('AuthContext: Is authenticated:', authenticated);
            
            setIsAuthenticated(authenticated);
            
            if (authenticated) {
                const userData = userUtils.getUserInfo();
                console.log('AuthContext: User data loaded:', !!userData);
                console.log('AuthContext: User data:', userData);
                setUserInfo(userData);
            } else {
                setUserInfo(null);
            }
        } catch (error) {
            console.error('AuthContext: Error checking auth status:', error);
            setIsAuthenticated(false);
            setUserInfo(null);
        } finally {
            console.log('AuthContext: Check complete');
            setIsLoading(false);
        }
    };

    useEffect(() => {
        console.log('AuthContext: Initial auth check');
        checkAuthStatus();
    }, []);

    const login = (token: string, userInfo: UserInfo) => {
        console.log('AuthContext: Login called');
        tokenUtils.setToken(token);
        userUtils.setUserInfo(userInfo);
        setIsAuthenticated(true);
        setUserInfo(userInfo);
        setIsLoading(false);
        console.log('AuthContext: Login complete, authenticated:', true);
    };

    const logout = () => {
        console.log('AuthContext: Logout called');
        tokenUtils.removeToken();
        userUtils.removeUserInfo();
        setIsAuthenticated(false);
        setUserInfo(null);
        console.log('AuthContext: Logout complete, authenticated:', false);
    };

    const updateUserInfo = (newUserInfo: UserInfo) => {
        userUtils.setUserInfo(newUserInfo);
        setUserInfo(newUserInfo);
    };

    const refreshAuth = () => {
        console.log('AuthContext: Manual refresh requested');
        setIsLoading(true);
        checkAuthStatus();
    };

    const value = {
        isAuthenticated,
        userInfo,
        isLoading,
        login,
        logout,
        updateUserInfo,
        refreshAuth
    };

    console.log('AuthContext: Providing context values:', { 
        isAuthenticated, 
        hasUserInfo: !!userInfo, 
        isLoading 
    });

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}; 