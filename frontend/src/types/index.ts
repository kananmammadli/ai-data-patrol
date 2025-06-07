export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'configurator' | 'viewer';
  is_active: boolean;
  is_verified: boolean;
  auth_provider: 'password' | 'google' | 'github';
  created_at: string;
  updated_at?: string;
} 