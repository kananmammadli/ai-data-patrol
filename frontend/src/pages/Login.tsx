import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/LoginForm';
import { authService } from '../services/authService';

export const Login: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // If already authenticated, redirect to home
    if (authService.isAuthenticated()) {
      navigate('/');
    }
  }, [navigate]);

  return <LoginForm />;
}; 