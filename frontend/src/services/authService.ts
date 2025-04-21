import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8003/api/v1';

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
      // The backend returns a 307 redirect, so we need to follow it
      window.location.href = `${API_URL}/auth/google`;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Google login failed');
      }
      throw error;
    }
  }

  public handleGoogleCallback(token: string): void {
    this.setToken(token);
  }

  public logout(): void {
    this.token = null;
    localStorage.removeItem('token');
  }

  public getToken(): string | null {
    return this.token;
  }

  public isAuthenticated(): boolean {
    return !!this.token;
  }

  private setToken(token: string): void {
    this.token = token;
    localStorage.setItem('token', token);
  }
}

export const authService = AuthService.getInstance(); 