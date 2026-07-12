
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SettingBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class SettingCreate(SettingBase):
    pass

class SettingUpdate(SettingBase):
    pass

class SettingResponse(SettingBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True