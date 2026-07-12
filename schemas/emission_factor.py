
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class EmissionFactorBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class EmissionFactorCreate(EmissionFactorBase):
    pass

class EmissionFactorUpdate(EmissionFactorBase):
    pass

class EmissionFactorResponse(EmissionFactorBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True