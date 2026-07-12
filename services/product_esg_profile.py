
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.product_esg_profile import product_esg_profile_repo
from schemas.product_esg_profile import ProductESGProfileCreate, ProductESGProfileUpdate
from models.product_esg_profile import ProductESGProfile

class ProductESGProfileService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ProductESGProfile]:
        return await product_esg_profile_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[ProductESGProfile]:
        return await product_esg_profile_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: ProductESGProfileCreate) -> ProductESGProfile:
        return await product_esg_profile_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: ProductESGProfileUpdate) -> Optional[ProductESGProfile]:
        db_obj = await product_esg_profile_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await product_esg_profile_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await product_esg_profile_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await product_esg_profile_repo.delete(db, id)
        return True