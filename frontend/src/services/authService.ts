    import axios from 'axios';
import { User } from '../types';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export class AuthService {
  private static instance: AuthService;
  private token: string | null = null;

  private constructor() {
    this.token = localStorage.getItem('token');
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async login(email: string, password: string): Promise<void> {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email,
        password,
      });
      this.setToken(response.data.access_token);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Login failed');
      }
      throw error;
    }
  }

  public async loginWithGoogle(): Promise<void> {
    try {
      console.log('Initiating Google login...');
      const response = await fetch(`${API_URL}/auth/google`);
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Google login failed:', errorData);
        throw new Error(errorData.detail || 'Failed to initiate Google login');
      }
      
      const data = await response.json();
      console.log('Redirecting to Google OAuth:', data.auth_url);
      window.location.href = data.auth_url;
    } catch (error) {
      console.error('Error during Google login:', error);
      throw error;
    }
  }

  public async handleGoogleCallback(token: string): Promise<void> {
    try {
        console.log('Handling Google callback with token:', token);
        this.setToken(token);
        
        // Verify the token is valid
        const response = await fetch(`${API_URL}/users/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,  // Add 'Bearer ' prefix
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Token verification failed:', errorData);
            console.error('Response status:', response.status);
            console.error('Response status text:', response.statusText);
            this.removeToken();
            throw new Error(errorData.detail || 'Invalid token');
        }

        const userData = await response.json();
        console.log('Successfully authenticated with Google:', userData);
        
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify(userData));
    } catch (error) {
        console.error('Error handling Google callback:', error);
        if (error instanceof Error) {
            console.error('Error message:', error.message);
            console.error('Error stack:', error.stack);
        }
        this.removeToken();
        localStorage.removeItem('user');
        throw error;
    }
  }

  public logout(): void {
    this.token = null;
    localStorage.removeItem('token');
  }

  public getToken(): string | null {
    return this.token;
  }

  public getUser(): any | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  public isAuthenticated(): boolean {
    return !!this.getToken() && !!this.getUser();
  }

  public async updatePassword(currentPassword: string, newPassword: string): Promise<void> {
    await axios.post(
      `${API_URL}/auth/password/update`,
      {
        current_password: currentPassword,
        new_password: newPassword,
      },
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      }
    );
  }

  public async requestPasswordReset(email: string): Promise<void> {
    await axios.post(`${API_URL}/auth/password/reset-request`, {
      email,
    });
  }

  public async resetPassword(token: string, newPassword: string): Promise<void> {
    await axios.post(`${API_URL}/auth/password/reset`, {
      token,
      new_password: newPassword,
    });
  }

  private setToken(token: string): void {
    this.token = token;
    localStorage.setItem('token', token);
  }

  private removeToken(): void {
    this.token = null;
    localStorage.removeItem('token');
  }
}

export const authService = AuthService.getInstance(); 