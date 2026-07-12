
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DepartmentScoreBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class DepartmentScoreCreate(DepartmentScoreBase):
    pass

class DepartmentScoreUpdate(DepartmentScoreBase):
    pass

class DepartmentScoreResponse(DepartmentScoreBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True