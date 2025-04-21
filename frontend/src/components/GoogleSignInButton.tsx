import React, { useState } from 'react';
import { Button, Alert } from '@mui/material';
import { authService } from '../services/authService';

declare global {
  interface Window {
    google: any;
  }
}

export const GoogleSignInButton: React.FC = () => {
  const [error, setError] = useState<string | null>(null);

  const handleGoogleSignIn = async () => {
    try {
      setError(null);
      await authService.loginWithGoogle();
    } catch (error) {
      console.error('Google sign-in failed:', error);
      setError(error instanceof Error ? error.message : 'Failed to sign in with Google');
    }
  };

  return (
    <>
      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <Button
        fullWidth
        variant="outlined"
        onClick={handleGoogleSignIn}
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 1,
        }}
      >
        <img
          src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
          alt="Google"
          width="18"
          height="18"
        />
        Sign in with Google
      </Button>
    </>
  );
};

export default GoogleSignInButton; 