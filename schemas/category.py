
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True