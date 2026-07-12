
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BadgeBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class BadgeCreate(BadgeBase):
    pass

class BadgeUpdate(BadgeBase):
    pass

class BadgeResponse(BadgeBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True