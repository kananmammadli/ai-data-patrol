from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.data_quality import DatabaseType, CheckStatus

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

class DataQualityCheckBase(BaseModel):
    name: str
    check_type: str
    check_params: Dict[str, Any]
    schedule: str

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
    result_data: Optional[Dict[str, Any]]

class DataQualityResultCreate(DataQualityResultBase):
    pass

class DataQualityResult(DataQualityResultBase):
    id: int
    executed_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True
