
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class EmployeeParticipationBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class EmployeeParticipationCreate(EmployeeParticipationBase):
    pass

class EmployeeParticipationUpdate(EmployeeParticipationBase):
    pass

class EmployeeParticipationResponse(EmployeeParticipationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True