import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box } from '@mui/material';
import UserManagement from './pages/UserManagement';

const App: React.FC = () => {
  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              AI Data Patrol
            </Typography>
            <Link to="/users" style={{ color: 'white', textDecoration: 'none' }}>
              Users
            </Link>
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Routes>
            <Route path="/users" element={<UserManagement />} />
            <Route path="/" element={<UserManagement />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
};

export default App; 