
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.notification import notification_repo
from schemas.notification import NotificationCreate, NotificationUpdate
from models.notification import Notification

class NotificationService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Notification]:
        return await notification_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Notification]:
        return await notification_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: NotificationCreate) -> Notification:
        return await notification_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: NotificationUpdate) -> Optional[Notification]:
        db_obj = await notification_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await notification_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await notification_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await notification_repo.delete(db, id)
        return True