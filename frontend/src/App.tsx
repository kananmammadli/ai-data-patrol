import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box, Button, ThemeProvider, CssBaseline, createTheme } from '@mui/material';
import UserManagement from './pages/UserManagement';
import { Login } from './pages/Login';
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

  useEffect(() => {
    const urlParams = new URLSearchParams(location.search);
    const token = urlParams.get('token');
    if (token) {
      authService.handleGoogleCallback(token);
    }
  }, [location]);

  return <Navigate to="/users" replace />;
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
              <Route
                path="/users"
                element={
                  <PrivateRoute>
                    <UserManagement />
                  </PrivateRoute>
                }
              />
              <Route
                path="/"
                element={
                  authService.isAuthenticated() ? (
                    <Navigate to="/users" replace />
                  ) : (
                    <Navigate to="/login" replace />
                  )
                }
              />
              <Route path="/auth/callback" element={<AuthCallbackHandler />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default App; 