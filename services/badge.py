
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.badge import badge_repo
from schemas.badge import BadgeCreate, BadgeUpdate
from models.badge import Badge

class BadgeService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Badge]:
        return await badge_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Badge]:
        return await badge_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: BadgeCreate) -> Badge:
        return await badge_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: BadgeUpdate) -> Optional[Badge]:
        db_obj = await badge_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await badge_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await badge_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await badge_repo.delete(db, id)
        return True