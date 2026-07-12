
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ComplianceIssueBase(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = "active"

class ComplianceIssueCreate(ComplianceIssueBase):
    pass

class ComplianceIssueUpdate(ComplianceIssueBase):
    pass

class ComplianceIssueResponse(ComplianceIssueBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    version: int
    
    class Config:
        from_attributes = True