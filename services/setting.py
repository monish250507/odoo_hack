
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.setting import setting_repo
from schemas.setting import SettingCreate, SettingUpdate
from models.setting import Setting

class SettingService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Setting]:
        return await setting_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Setting]:
        return await setting_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: SettingCreate) -> Setting:
        return await setting_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: SettingUpdate) -> Optional[Setting]:
        db_obj = await setting_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await setting_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await setting_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await setting_repo.delete(db, id)
        return True