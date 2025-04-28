from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum
from app.core.security import get_password_hash, verify_password
from app.db.session import Base
from app.models.enums import UserRole, AuthProvider

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    auth_provider = Column(SQLEnum(AuthProvider), default=AuthProvider.PASSWORD)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        if not self.hashed_password:
            return False
        return verify_password(password, self.hashed_password)

    def __repr__(self):
        return f"<User {self.email}>" 