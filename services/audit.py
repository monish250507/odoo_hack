
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.audit import audit_repo
from schemas.audit import AuditCreate, AuditUpdate
from models.audit import Audit

class AuditService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Audit]:
        return await audit_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Audit]:
        return await audit_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: AuditCreate) -> Audit:
        return await audit_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: AuditUpdate) -> Optional[Audit]:
        db_obj = await audit_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await audit_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await audit_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await audit_repo.delete(db, id)
        return True