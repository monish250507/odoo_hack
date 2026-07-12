
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class RewardBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class RewardCreate(RewardBase):
    pass

class RewardUpdate(RewardBase):
    pass

class RewardResponse(RewardBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True