
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True