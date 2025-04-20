import React, { useEffect, useState } from 'react';
import { userService, User, CreateUserData, UpdateUserData } from '../services/userService';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  IconButton,
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import UserForm from '../components/UserForm';

interface PaginatedResponse {
  users: User[];
  total: number;
  page: number;
  size: number;
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    size: 100
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await userService.getUsers();
      
      // Check if response is a paginated response
      if (response && typeof response === 'object' && 'users' in response) {
        const paginatedResponse = response as unknown as PaginatedResponse;
        setUsers(paginatedResponse.users);
        setPagination({
          total: paginatedResponse.total,
          page: paginatedResponse.page,
          size: paginatedResponse.size
        });
      } else {
        console.error('Invalid data format received:', response);
        setError('Invalid data format received from server');
        setUsers([]);
      }
    } catch (err) {
      setError('Failed to fetch users. Please try again later.');
      console.error('Error fetching users:', err);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      setError(null);
      await userService.deleteUser(id);
      setUsers(prevUsers => prevUsers.filter(user => user.id !== id));
    } catch (err) {
      setError('Failed to delete user. Please try again later.');
      console.error('Error deleting user:', err);
    }
  };

  const handleCreateUser = async (data: CreateUserData) => {
    try {
      setError(null);
      const newUser = await userService.createUser(data);
      setUsers(prevUsers => [...prevUsers, newUser]);
      setOpenDialog(false);
    } catch (err) {
      setError('Failed to create user. Please try again later.');
      console.error('Error creating user:', err);
    }
  };

  const handleUpdateUser = async (data: UpdateUserData) => {
    if (!selectedUser) return;
    try {
      setError(null);
      const updatedUser = await userService.updateUser(selectedUser.id, data);
      setUsers(prevUsers => prevUsers.map(user => user.id === updatedUser.id ? updatedUser : user));
      setOpenDialog(false);
      setSelectedUser(null);
    } catch (err) {
      setError('Failed to update user. Please try again later.');
      console.error('Error updating user:', err);
    }
  };

  const handleEditClick = (user: User) => {
    setSelectedUser(user);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedUser(null);
  };

  const handleFormSubmit = async (data: CreateUserData | UpdateUserData) => {
    if (selectedUser) {
      await handleUpdateUser(data as UpdateUserData);
    } else {
      await handleCreateUser(data as CreateUserData);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">User Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Add User
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  <Typography>No users found</Typography>
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{`${user.first_name} ${user.last_name}`}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.role}</TableCell>
                  <TableCell>{user.is_active ? 'Active' : 'Inactive'}</TableCell>
                  <TableCell>
                    <IconButton color="primary" onClick={() => handleEditClick(user)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton color="error" onClick={() => handleDelete(user.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedUser ? 'Edit User' : 'Create New User'}
        </DialogTitle>
        <DialogContent>
          <UserForm
            initialData={selectedUser}
            onSubmit={handleFormSubmit}
            isEdit={!!selectedUser}
          />
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default UserManagement; 