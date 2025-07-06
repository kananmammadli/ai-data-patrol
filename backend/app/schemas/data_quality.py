from pydantic import BaseModel, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..models.data_quality import DatabaseType, CheckStatus, SeverityLevel

class DatabaseConnectionBase(BaseModel):
    name: str
    type: DatabaseType
    connection_params: Dict[str, Any]

class DatabaseConnectionCreate(DatabaseConnectionBase):
    pass

class DatabaseConnection(DatabaseConnectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrganizationNodeBase(BaseModel):
    name: str
    type: str  # 'department' or 'project'
    parent_id: Optional[int] = None
    description: Optional[str] = None

class OrganizationNodeCreate(OrganizationNodeBase):
    pass

class OrganizationNode(OrganizationNodeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: Optional[list['OrganizationNode']] = []

    class Config:
        orm_mode = True

class DataQualityCheckBase(BaseModel):
    name: str
    check_type: str
    check_params: Dict[str, Any]
    schedule: str
    expiry_period: Optional[int] = None
    tags: Optional[list[str]] = None
    organization_node_id: Optional[int] = None  # FK to OrganizationNode
    troubleshooting: Optional[str] = None

class DataQualityCheckCreate(DataQualityCheckBase):
    database_id: int

class DataQualityCheck(DataQualityCheckBase):
    id: int
    database_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DataQualityResultBase(BaseModel):
    check_id: int
    status: CheckStatus
    severity: int = 0  # 0 means normal, output of check script
    recipients: Optional[list[str]] = None  # based on severity
    result_data: Optional[Dict[str, Any]]

class DataQualityResultCreate(DataQualityResultBase):
    pass

class DataQualityResult(DataQualityResultBase):
    id: int
    executed_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True

class SeverityConfigBase(BaseModel):
    severity: int
    recipients: list[str]
    threshold: int = 0

class SeverityConfigCreate(SeverityConfigBase):
    check_id: int

class SeverityConfig(SeverityConfigBase):
    id: int
    check_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
