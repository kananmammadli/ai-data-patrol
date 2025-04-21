from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from datetime import datetime
from ..models import UserRole, AuthProvider

class UserBase(BaseModel):
    email: EmailStr
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    is_verified: bool = False

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserCreate(UserBase):
    password: Optional[constr(min_length=8)] = None
    auth_provider: AuthProvider = AuthProvider.PASSWORD

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[constr(min_length=1, max_length=50)] = None
    last_name: Optional[constr(min_length=1, max_length=50)] = None
    password: Optional[constr(min_length=8)] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: UUID
    auth_provider: AuthProvider
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(UserInDB):
    pass

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int

class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 