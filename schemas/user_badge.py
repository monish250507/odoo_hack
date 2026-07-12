
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserBadgeBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class UserBadgeCreate(UserBadgeBase):
    pass

class UserBadgeUpdate(UserBadgeBase):
    pass

class UserBadgeResponse(UserBadgeBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True