import axios from 'axios';

// Настройка axios для работы с бэкендом
// Используем относительные URL благодаря прокси в vite.config.ts
export const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для автоматического добавления токена к запросам
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Интерцептор для обработки ответов
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Удаляем токен и перенаправляем на страницу входа
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

// Типы для API запросов
export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name: string;
}

export interface SurveyData {
  name: string;
  surname: string;
  country: string;
  city: string;
  gender: string;
  age: number;
  height: number;
}



// API функции для аутентификации
export const authAPI = {
  login: async (data: LoginData) => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterData) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  verifyToken: async () => {
    const response = await api.get('/auth/verify-token');
    return response.data;
  }
};

// API функции для пользователей
export const userAPI = {
  updateTrainingProfile: async (data: any) => {
    const response = await api.put('/auth/training-profile', data);
    return response.data;
  },

  getTrainingProfile: async () => {
    const response = await api.get('/auth/training-profile');
    return response.data;
  }
};



// Утилитарные функции
export const authUtils = {
  saveAuthData: (token: string, userInfo: any) => {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user_info', JSON.stringify(userInfo));
  },

  getAuthData: () => {
    const token = localStorage.getItem('auth_token');
    const userInfo = localStorage.getItem('user_info');
    return {
      token,
      userInfo: userInfo ? JSON.parse(userInfo) : null
    };
  },

  clearAuthData: () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_info');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('auth_token');
  }
}; 