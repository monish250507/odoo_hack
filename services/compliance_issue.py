
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.compliance_issue import compliance_issue_repo
from schemas.compliance_issue import ComplianceIssueCreate, ComplianceIssueUpdate
from models.compliance_issue import ComplianceIssue

class ComplianceIssueService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ComplianceIssue]:
        return await compliance_issue_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[ComplianceIssue]:
        return await compliance_issue_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: ComplianceIssueCreate) -> ComplianceIssue:
        return await compliance_issue_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: ComplianceIssueUpdate) -> Optional[ComplianceIssue]:
        db_obj = await compliance_issue_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await compliance_issue_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await compliance_issue_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await compliance_issue_repo.delete(db, id)
        return True