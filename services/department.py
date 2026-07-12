
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.department import department_repo
from schemas.department import DepartmentCreate, DepartmentUpdate
from models.department import Department

class DepartmentService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Department]:
        return await department_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[Department]:
        return await department_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: DepartmentCreate) -> Department:
        return await department_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: DepartmentUpdate) -> Optional[Department]:
        db_obj = await department_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await department_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await department_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await department_repo.delete(db, id)
        return True