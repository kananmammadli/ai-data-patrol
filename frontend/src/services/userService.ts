import axios from 'axios';
import { authService } from './authService';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'configurator' | 'viewer';
  is_active: boolean;
  is_verified: boolean;
  auth_provider: 'password' | 'google' | 'github';
  created_at: string;
  updated_at?: string;
}

export interface CreateUserData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'configurator' | 'viewer';
  is_active?: boolean;
}

export interface UpdateUserData {
  first_name?: string;
  last_name?: string;
  role?: 'admin' | 'configurator' | 'viewer';
  email?: string;
  password?: string;
  is_active?: boolean;
}

export interface UserListResponse {
  users: User[];
  total: number;
  page: number;
  size: number;
}

class UserService {
  async getUsers(): Promise<UserListResponse> {
    try {
      const response = await api.get('/users/');
      return response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  }

  async getUserById(id: string): Promise<User> {
    try {
      const response = await api.get(`/users/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching user ${id}:`, error);
      throw error;
    }
  }

  async createUser(data: CreateUserData): Promise<User> {
    try {
      const response = await api.post('/users/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  }

  async updateUser(id: string, data: UpdateUserData): Promise<User> {
    try {
      // If password is being updated, use the dedicated password update endpoint
      if (data.password) {
        await api.post(`/users/${id}/password`, { password: data.password });
        // Remove password from data to avoid sending it in the user update
        delete data.password;
      }
      
      // Update other user fields if any
      if (Object.keys(data).length > 0) {
        const response = await api.put(`/users/${id}`, data);
        return response.data;
      } else {
        // If only password was updated, get the latest user data
        const response = await api.get(`/users/${id}`);
        return response.data;
      }
    } catch (error) {
      console.error(`Error updating user ${id}:`, error);
      throw error;
    }
  }

  async deleteUser(id: string): Promise<void> {
    try {
      await api.delete(`/users/${id}/`);
    } catch (error) {
      console.error(`Error deleting user ${id}:`, error);
      throw error;
    }
  }

  async getCurrentUser(): Promise<User> {
    try {
      const response = await api.get('/users/me');
      return response.data;
    } catch (error) {
      console.error('Error fetching current user:', error);
      throw error;
    }
  }
}

export const userService = new UserService(); 