from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..core.database import Base

class DatabaseType(str, enum.Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SNOWFLAKE = "snowflake"

class CheckStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ERROR = "error"

class SeverityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DatabaseConnection(Base):
    __tablename__ = "database_connections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(SQLEnum(DatabaseType))
    connection_params = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    checks = relationship("DataQualityCheck", back_populates="database")

class DataQualityCheck(Base):
    __tablename__ = "data_quality_checks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    database_id = Column(Integer, ForeignKey("database_connections.id"))
    check_type = Column(String)  # e.g., "completeness", "accuracy", "consistency"
    check_params = Column(JSON)
    schedule = Column(String)  # cron expression
    expiry_period = Column(Integer, nullable=True)  # in minutes or seconds
    tags = Column(JSON, nullable=True)  # list of tags
    organization = Column(String, nullable=True)  # department/project
    troubleshooting = Column(String, nullable=True)  # troubleshooting instructions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    database = relationship("DatabaseConnection", back_populates="checks")
    results = relationship("DataQualityResult", back_populates="check")

class DataQualityResult(Base):
    __tablename__ = "data_quality_results"

    id = Column(Integer, primary_key=True, index=True)
    check_id = Column(Integer, ForeignKey("data_quality_checks.id"))
    status = Column(SQLEnum(CheckStatus))
    severity = Column(Integer, default=0)  # 0 means normal, output of check script
    recipients = Column(JSON, nullable=True)  # list of recipients, based on severity
    result_data = Column(JSON)
    executed_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    check = relationship("DataQualityCheck", back_populates="results")
