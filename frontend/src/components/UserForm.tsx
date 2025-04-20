import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Typography,
  SelectChangeEvent,
} from '@mui/material';
import { CreateUserData, UpdateUserData, User } from '../services/userService';

interface UserFormProps {
  initialData?: User | null;
  onSubmit: (data: CreateUserData | UpdateUserData) => Promise<void>;
  isEdit?: boolean;
}

const UserForm: React.FC<UserFormProps> = ({ initialData, onSubmit, isEdit = false }) => {
  const [formData, setFormData] = useState<CreateUserData | UpdateUserData>(
    isEdit
      ? {
          first_name: initialData?.first_name || '',
          last_name: initialData?.last_name || '',
          role: initialData?.role || 'viewer',
        }
      : {
          email: '',
          password: '',
          first_name: '',
          last_name: '',
          role: 'viewer',
        }
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSelectChange = (e: SelectChangeEvent) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        {isEdit ? 'Edit User' : 'Create New User'}
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            fullWidth
            label="First Name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            fullWidth
            label="Last Name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </Grid>
        {!isEdit && (
          <>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Email"
                name="email"
                type="email"
                value={(formData as CreateUserData).email}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Password"
                name="password"
                type="password"
                value={(formData as CreateUserData).password}
                onChange={handleChange}
              />
            </Grid>
          </>
        )}
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Role</InputLabel>
            <Select
              name="role"
              value={formData.role}
              label="Role"
              onChange={handleSelectChange}
            >
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="configurator">Configurator</MenuItem>
              <MenuItem value="viewer">Viewer</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <Button type="submit" variant="contained" color="primary">
            {isEdit ? 'Update User' : 'Create User'}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default UserForm; 