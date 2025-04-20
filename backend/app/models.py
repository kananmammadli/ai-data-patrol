from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CONFIGURATOR = "configurator"
    VIEWER = "viewer"

class AuthProvider(str, enum.Enum):
    GOOGLE = "google"
    OKTA = "okta"
    PASSWORD = "password"

class TimestampMixin:
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    
    # Authentication fields
    auth_provider = Column(SQLEnum(AuthProvider), nullable=False, default=AuthProvider.PASSWORD)
    hashed_password = Column(String, nullable=True)  # Nullable because not needed for OAuth users
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # OAuth related fields
    oauth_id = Column(String, nullable=True)  # ID from OAuth provider
    oauth_access_token = Column(String, nullable=True)
    oauth_refresh_token = Column(String, nullable=True)
    oauth_token_expires_at = Column(DateTime, nullable=True)

class DBConnection(Base, TimestampMixin):
    __tablename__ = "db_connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    database = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)

class DataCheck(Base, TimestampMixin):
    __tablename__ = "data_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    project = Column(String, nullable=False)
    description = Column(Text)
    troubleshooting_guide = Column(Text)
    db_connection_id = Column(UUID(as_uuid=True), ForeignKey("db_connections.id"), nullable=False)
    sql_script = Column(Text, nullable=False)
    schedule = Column(String, nullable=False)  # cron-style string
    expiry_period_hours = Column(Integer, nullable=False)
    max_attachment_rows = Column(Integer, default=100)

    db_connection = relationship("DBConnection")
    severity_recipients = relationship("SeverityRecipient", back_populates="data_check")
    check_runs = relationship("CheckRun", back_populates="data_check")

class SeverityRecipient(Base, TimestampMixin):
    __tablename__ = "severity_recipients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_check_id = Column(UUID(as_uuid=True), ForeignKey("data_checks.id"), nullable=False)
    min_severity = Column(Integer, nullable=False)
    max_severity = Column(Integer, nullable=False)
    emails = Column(String, nullable=False)  # Comma-separated list of emails

    data_check = relationship("DataCheck", back_populates="severity_recipients")

class CheckRun(Base, TimestampMixin):
    __tablename__ = "check_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_check_id = Column(UUID(as_uuid=True), ForeignKey("data_checks.id"), nullable=False)
    run_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    severity = Column(Integer, nullable=False)
    result_preview = Column(Text)  # CSV format
    notified = Column(Boolean, default=False)
    notification_timestamp = Column(DateTime, nullable=True)

    data_check = relationship("DataCheck", back_populates="check_runs") 