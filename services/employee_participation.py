
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.employee_participation import employee_participation_repo
from schemas.employee_participation import EmployeeParticipationCreate, EmployeeParticipationUpdate
from models.employee_participation import EmployeeParticipation

class EmployeeParticipationService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[EmployeeParticipation]:
        return await employee_participation_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[EmployeeParticipation]:
        return await employee_participation_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: EmployeeParticipationCreate) -> EmployeeParticipation:
        return await employee_participation_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: EmployeeParticipationUpdate) -> Optional[EmployeeParticipation]:
        db_obj = await employee_participation_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await employee_participation_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await employee_participation_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await employee_participation_repo.delete(db, id)
        return True