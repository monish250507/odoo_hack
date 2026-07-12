
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ChallengeBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(ChallengeBase):
    pass

class ChallengeResponse(ChallengeBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True