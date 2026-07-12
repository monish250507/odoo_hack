
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ChallengeParticipationBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class ChallengeParticipationCreate(ChallengeParticipationBase):
    pass

class ChallengeParticipationUpdate(ChallengeParticipationBase):
    pass

class ChallengeParticipationResponse(ChallengeParticipationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True