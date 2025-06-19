import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authAPI, authUtils } from '../services/api';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, fullName: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  // Проверяем аутентификацию при загрузке
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { token, userInfo } = authUtils.getAuthData();
        if (token) {
          // Сначала устанавливаем данные из localStorage (если есть)
          if (userInfo) {
            setUser(userInfo);
            setIsAuthenticated(true);
          }
          
          // Затем проверяем валидность токена и обновляем данные
          try {
            const response = await authAPI.getCurrentUser();
            setUser(response.user_info); // Извлекаем user_info из ответа
            setIsAuthenticated(true);
          } catch (apiError) {
            // Если API недоступен, но токен есть, используем данные из localStorage
            if (userInfo) {
              console.warn('API недоступен, используем данные из localStorage');
            } else {
              throw apiError;
            }
          }
        }
      } catch (error) {
        // Токен недействителен, очищаем данные
        authUtils.clearAuthData();
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await authAPI.login({ username, password });
      authUtils.saveAuthData(response.access_token, response.user_info);
      setUser(response.user_info);
      setIsAuthenticated(true);
    } catch (error) {
      throw error;
    }
  };

  const register = async (username: string, email: string, password: string, fullName: string) => {
    try {
      const response = await authAPI.register({
        username,
        email,
        password,
        full_name: fullName
      });
      // После регистрации автоматически входим
      await login(username, password);
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      // Игнорируем ошибки при выходе
    } finally {
      authUtils.clearAuthData();
      setIsAuthenticated(false);
      setUser(null);
    }
  };

  const refreshUser = async () => {
    try {
      if (isAuthenticated) {
        const response = await authAPI.getCurrentUser();
        setUser(response.user_info); // Извлекаем user_info из ответа
      }
    } catch (error) {
      console.error('Error refreshing user data:', error);
    }
  };

  const value = {
    isAuthenticated,
    user,
    login,
    register,
    logout,
    refreshUser,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 