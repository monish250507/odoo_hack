
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PolicyAcknowledgementBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class PolicyAcknowledgementCreate(PolicyAcknowledgementBase):
    pass

class PolicyAcknowledgementUpdate(PolicyAcknowledgementBase):
    pass

class PolicyAcknowledgementResponse(PolicyAcknowledgementBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True