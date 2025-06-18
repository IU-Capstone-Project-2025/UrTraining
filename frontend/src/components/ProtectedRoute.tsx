import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

interface ProtectedRouteProps {
    children: React.ReactNode
    redirectTo?: string
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
    children, 
    redirectTo = '/signin' 
}) => {
    const { isAuthenticated, isLoading } = useAuth()
    
    console.log('ProtectedRoute: Auth status:', { isAuthenticated, isLoading });
    
    // Show loading spinner while checking authentication
    if (isLoading) {
        console.log('ProtectedRoute: Still loading, showing loading screen');
        return (
            <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '100vh',
                fontSize: '18px'
            }}>
                Loading...
            </div>
        )
    }
    
    if (!isAuthenticated) {
        console.log('ProtectedRoute: Not authenticated, redirecting to:', redirectTo);
        return <Navigate to={redirectTo} replace />
    }
    
    console.log('ProtectedRoute: Authenticated, rendering protected content');
    return <>{children}</>
}

export default ProtectedRoute 