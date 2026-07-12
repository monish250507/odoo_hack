
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AuditBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class AuditCreate(AuditBase):
    pass

class AuditUpdate(AuditBase):
    pass

class AuditResponse(AuditBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True