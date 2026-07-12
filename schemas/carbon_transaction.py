
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CarbonTransactionBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class CarbonTransactionCreate(CarbonTransactionBase):
    pass

class CarbonTransactionUpdate(CarbonTransactionBase):
    pass

class CarbonTransactionResponse(CarbonTransactionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True