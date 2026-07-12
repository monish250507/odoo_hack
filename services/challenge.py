
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.challenge import challenge_repo
from schemas.challenge import ChallengeCreate, ChallengeUpdate
from models.challenge import Challenge

class ChallengeService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Challenge]:
        return await challenge_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Challenge]:
        return await challenge_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: ChallengeCreate) -> Challenge:
        return await challenge_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: ChallengeUpdate) -> Optional[Challenge]:
        db_obj = await challenge_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await challenge_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await challenge_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await challenge_repo.delete(db, id)
        return True