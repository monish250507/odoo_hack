
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ProductESGProfileBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class ProductESGProfileCreate(ProductESGProfileBase):
    pass

class ProductESGProfileUpdate(ProductESGProfileBase):
    pass

class ProductESGProfileResponse(ProductESGProfileBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True