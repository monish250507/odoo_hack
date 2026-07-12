
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PolicyBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(PolicyBase):
    pass

class PolicyResponse(PolicyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True