
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True