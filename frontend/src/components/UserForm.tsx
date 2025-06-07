import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Switch,
  FormControlLabel,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { CreateUserData, UpdateUserData, User } from '../services/userService';

interface UserFormProps {
  initialData?: User;
  onSubmit: (data: CreateUserData | UpdateUserData) => Promise<void>;
  isEdit?: boolean;
  isAdmin?: boolean;
}

const UserForm: React.FC<UserFormProps> = ({ 
  initialData, 
  onSubmit, 
  isEdit = false,
  isAdmin = false 
}) => {
  const [formData, setFormData] = useState<CreateUserData | UpdateUserData>(
    isEdit
      ? {
          first_name: initialData?.first_name || '',
          last_name: initialData?.last_name || '',
          role: initialData?.role || 'viewer',
          email: initialData?.email || '',
          is_active: initialData?.is_active ?? true,
          ...(isAdmin && { password: '' })
        }
      : {
          email: '',
          password: '',
          first_name: '',
          last_name: '',
          role: 'viewer',
          is_active: true
        }
  );
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSelectChange = (e: SelectChangeEvent) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
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
        {(isAdmin || !isEdit) && (
          <Grid item xs={12}>
            <TextField
              required
              fullWidth
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              disabled={isEdit && !isAdmin}
            />
          </Grid>
        )}
        {(isAdmin || !isEdit) && (
          <Grid item xs={12}>
            <TextField
              required={!isEdit}
              fullWidth
              label="Password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password || ''}
              onChange={handleChange}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
        )}
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Role</InputLabel>
            <Select
              name="role"
              value={formData.role}
              label="Role"
              onChange={handleSelectChange}
              disabled={!isAdmin}
            >
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="configurator">Configurator</MenuItem>
              <MenuItem value="viewer">Viewer</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        {isAdmin && isEdit && (
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_active}
                  onChange={handleChange}
                  name="is_active"
                />
              }
              label="Active"
            />
          </Grid>
        )}
        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
          >
            {isEdit ? 'Update User' : 'Create User'}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default UserForm; 