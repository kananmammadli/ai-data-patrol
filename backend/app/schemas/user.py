from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, Field
from uuid import UUID
from datetime import datetime
from app.models.user import AuthProvider, UserRole
import uuid

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.VIEWER
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    auth_provider: Optional[AuthProvider] = AuthProvider.PASSWORD

    class Config:
        from_attributes = True
        json_encoders = {
            AuthProvider: lambda v: v.value if v else None
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserCreate(UserBase):
    id: Optional[UUID] = Field(default_factory=lambda: str(uuid.uuid4()))
    password: Optional[constr(min_length=8)] = None

class UserUpdate(UserBase):
    password: Optional[constr(min_length=8)] = None

class UserInDB(UserBase):
    id: UUID
    hashed_password: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int

class User(UserInDB):
    pass

class PasswordUpdate(BaseModel):
    current_password: constr(min_length=8)
    new_password: constr(min_length=8)

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=8) 