import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box, Button, ThemeProvider, CssBaseline, createTheme, CircularProgress } from '@mui/material';
import UserManagement from './pages/UserManagement';
import { Login } from './pages/Login';
import { PasswordResetForm } from './components/PasswordResetForm';
import { PasswordUpdateForm } from './components/PasswordUpdateForm';
import Home from './pages/Home';
import { authService } from './services/authService';

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return authService.isAuthenticated() ? <>{children}</> : <Navigate to="/login" />;
};

const AuthCallbackHandler: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  React.useEffect(() => {
    const handleCallback = async () => {
      try {
        const urlParams = new URLSearchParams(location.search);
        const token = urlParams.get('token');
        
        if (!token) {
          console.error('No token found in callback URL');
          navigate('/login');
          return;
        }

        console.log('Processing auth callback...');
        await authService.handleGoogleCallback(token);
        console.log('Auth callback processed successfully');
        
        // Navigate to home page after successful authentication
        navigate('/', { replace: true });
      } catch (error) {
        console.error('Error processing auth callback:', error);
        // Show error message to user
        alert('Authentication failed. Please try again.');
        navigate('/login', { replace: true });
      }
    };

    handleCallback();
  }, [location, navigate]);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        p: 2,
      }}
    >
      <CircularProgress />
      <Typography variant="h6" sx={{ mt: 2 }}>
        Processing authentication...
      </Typography>
    </Box>
  );
};

const App: React.FC = () => {
  const handleLogout = () => {
    authService.logout();
    window.location.href = '/login';
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                AI Data Patrol
              </Typography>
              {authService.isAuthenticated() && (
                <>
                  <Link to="/users" style={{ color: 'white', textDecoration: 'none', marginRight: '20px' }}>
                    Users
                  </Link>
                  <Button color="inherit" onClick={handleLogout}>
                    Logout
                  </Button>
                </>
              )}
            </Toolbar>
          </AppBar>
          <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/auth/callback" element={<AuthCallbackHandler />} />
              <Route
                path="/"
                element={
                  <PrivateRoute>
                    <Home />
                  </PrivateRoute>
                }
              />
              <Route
                path="/users"
                element={
                  <PrivateRoute>
                    <UserManagement />
                  </PrivateRoute>
                }
              />
              <Route
                path="/password/reset"
                element={
                  <PrivateRoute>
                    <PasswordResetForm />
                  </PrivateRoute>
                }
              />
              <Route
                path="/password/update"
                element={
                  <PrivateRoute>
                    <PasswordUpdateForm />
                  </PrivateRoute>
                }
              />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default App; 