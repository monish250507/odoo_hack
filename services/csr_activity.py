
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.csr_activity import csr_activity_repo
from schemas.csr_activity import CSRActivityCreate, CSRActivityUpdate
from models.csr_activity import CSRActivity

class CSRActivityService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[CSRActivity]:
        return await csr_activity_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[CSRActivity]:
        return await csr_activity_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: CSRActivityCreate) -> CSRActivity:
        return await csr_activity_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: CSRActivityUpdate) -> Optional[CSRActivity]:
        db_obj = await csr_activity_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await csr_activity_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await csr_activity_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await csr_activity_repo.delete(db, id)
        return True