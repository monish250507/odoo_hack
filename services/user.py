
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import user_repo
from schemas.user import UserCreate, UserUpdate
from models.user import User

class UserService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        return await user_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[User]:
        return await user_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: UserCreate) -> User:
        return await user_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: UserUpdate) -> Optional[User]:
        db_obj = await user_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await user_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await user_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await user_repo.delete(db, id)
        return True