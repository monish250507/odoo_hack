
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class NotificationBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True