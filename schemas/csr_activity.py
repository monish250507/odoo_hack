
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CSRActivityBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class CSRActivityCreate(CSRActivityBase):
    pass

class CSRActivityUpdate(CSRActivityBase):
    pass

class CSRActivityResponse(CSRActivityBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True