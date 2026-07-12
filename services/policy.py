
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.policy import policy_repo
from schemas.policy import PolicyCreate, PolicyUpdate
from models.policy import Policy

class PolicyService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Policy]:
        return await policy_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Policy]:
        return await policy_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: PolicyCreate) -> Policy:
        return await policy_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: PolicyUpdate) -> Optional[Policy]:
        db_obj = await policy_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await policy_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await policy_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await policy_repo.delete(db, id)
        return True