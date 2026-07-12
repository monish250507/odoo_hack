
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class GoalBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class GoalCreate(GoalBase):
    pass

class GoalUpdate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True