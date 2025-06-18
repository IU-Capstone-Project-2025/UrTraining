// Authentication utility functions
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

export interface UserInfo {
    username: string;
    email: string;
    full_name: string;
    training_profile?: TrainingProfile;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
    user_info: UserInfo;
}

export interface RegisterResponse {
    message: string;
    user_info: UserInfo;
}

export interface TrainingProfile {
    basic_information: {
        gender?: string;
        age?: number;
        height_cm?: number;
        weight_kg?: number;
    };
    training_goals: string[];
    training_experience: {
        level?: string;
        frequency_last_3_months?: string;
    };
    preferences: {
        training_location?: string;
        location_details?: string;
        session_duration?: string;
    };
    health: {
        joint_back_problems?: boolean;
        chronic_conditions?: boolean;
        health_details?: string;
    };
    training_types: {
        strength_training?: number;
        cardio?: number;
        hiit?: number;
        yoga_pilates?: number;
        functional_training?: number;
        stretching?: number;
    };
}

export interface TrainingProfileUpdate {
    // Basic Information
    gender?: string;
    age?: number;
    height_cm?: number;
    weight_kg?: number;
    
    // Training Goals
    training_goals?: string[];
    
    // Training Experience
    training_level?: string;
    frequency_last_3_months?: string;
    
    // Preferences
    training_location?: string;
    location_details?: string;
    session_duration?: string;
    
    // Health
    joint_back_problems?: boolean;
    chronic_conditions?: boolean;
    health_details?: string;
    
    // Training Types (1-5 scale)
    strength_training?: number;
    cardio?: number;
    hiit?: number;
    yoga_pilates?: number;
    functional_training?: number;
    stretching?: number;
}

const API_BASE_URL = 'http://localhost:8000';

export const authAPI = {
    async login(data: LoginData): Promise<LoginResponse> {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Login failed');
        }
        
        return result;
    },

    async register(data: RegisterData): Promise<RegisterResponse> {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Registration failed');
        }
        
        return result;
    },

    async logout(): Promise<void> {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                await fetch(`${API_BASE_URL}/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
        
        // Clear local storage regardless of API call success
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
    },

    async getCurrentUser(): Promise<UserInfo | null> {
        const token = localStorage.getItem('access_token');
        if (!token) {
            return null;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get user info');
            }

            return await response.json();
        } catch (error) {
            console.error('Get current user error:', error);
            // Token might be expired, clear it
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
            return null;
        }
    },

    async updateTrainingProfile(data: TrainingProfileUpdate): Promise<{ message: string; training_profile: TrainingProfile }> {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/auth/training-profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Failed to update training profile');
        }
        
        return result;
    },

    async getTrainingProfile(): Promise<{ username: string; full_name: string; email: string; training_profile: TrainingProfile }> {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/auth/training-profile`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Failed to get training profile');
        }
        
        return result;
    }
};

export const tokenUtils = {
    getToken(): string | null {
        return localStorage.getItem('access_token');
    },

    setToken(token: string): void {
        localStorage.setItem('access_token', token);
    },

    removeToken(): void {
        localStorage.removeItem('access_token');
    },

    isAuthenticated(): boolean {
        return !!this.getToken();
    }
};

export const userUtils = {
    getUserInfo(): UserInfo | null {
        const userInfoStr = localStorage.getItem('user_info');
        if (!userInfoStr) {
            return null;
        }
        
        try {
            return JSON.parse(userInfoStr);
        } catch (error) {
            console.error('Error parsing user info:', error);
            localStorage.removeItem('user_info');
            return null;
        }
    },

    setUserInfo(userInfo: UserInfo): void {
        localStorage.setItem('user_info', JSON.stringify(userInfo));
    },

    removeUserInfo(): void {
        localStorage.removeItem('user_info');
    }
}; 