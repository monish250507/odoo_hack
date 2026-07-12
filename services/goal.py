
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.goal import goal_repo
from schemas.goal import GoalCreate, GoalUpdate
from models.goal import Goal

class GoalService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Goal]:
        return await goal_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Goal]:
        return await goal_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: GoalCreate) -> Goal:
        return await goal_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: GoalUpdate) -> Optional[Goal]:
        db_obj = await goal_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await goal_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await goal_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await goal_repo.delete(db, id)
        return True