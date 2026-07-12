from typing import Any, Generic, TypeVar, Type, Optional, Sequence
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        
        # If model supports soft delete, filter it out
        if hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
            
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        stmt = select(self.model)
        
        if hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
            
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: dict) -> ModelType:
        # Optimistic locking is handled automatically by SQLAlchemy if version_id_col is set
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: Any, hard: bool = False) -> None:
        db_obj = await self.get_by_id(db, id)
        if not db_obj:
            return
            
        if hard or not hasattr(self.model, "is_deleted"):
            await db.delete(db_obj)
        else:
            setattr(db_obj, "is_deleted", True)
            setattr(db_obj, "deleted_at", datetime.now(timezone.utc))
        
        await db.commit()
