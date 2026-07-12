
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.reward import reward_repo
from schemas.reward import RewardCreate, RewardUpdate
from models.reward import Reward

class RewardService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Reward]:
        return await reward_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Reward]:
        return await reward_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: RewardCreate) -> Reward:
        return await reward_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: RewardUpdate) -> Optional[Reward]:
        db_obj = await reward_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await reward_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await reward_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await reward_repo.delete(db, id)
        return True