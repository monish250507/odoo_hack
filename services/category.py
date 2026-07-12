
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.category import category_repo
from schemas.category import CategoryCreate, CategoryUpdate
from models.category import Category

class CategoryService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
        return await category_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Category]:
        return await category_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: CategoryCreate) -> Category:
        return await category_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: CategoryUpdate) -> Optional[Category]:
        db_obj = await category_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await category_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await category_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await category_repo.delete(db, id)
        return True