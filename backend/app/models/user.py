from sqlalchemy import Column, String, Boolean, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from ..database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CONFIGURATOR = "configurator"
    VIEWER = "viewer"

class AuthProvider(str, enum.Enum):
    PASSWORD = "password"
    GOOGLE = "google"
    GITHUB = "github"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    auth_provider = Column(Enum(AuthProvider), nullable=False, default=AuthProvider.PASSWORD)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>" 