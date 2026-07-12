
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.carbon_transaction import carbon_transaction_repo
from schemas.carbon_transaction import CarbonTransactionCreate, CarbonTransactionUpdate
from models.carbon_transaction import CarbonTransaction

class CarbonTransactionService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[CarbonTransaction]:
        return await carbon_transaction_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[CarbonTransaction]:
        return await carbon_transaction_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: CarbonTransactionCreate) -> CarbonTransaction:
        return await carbon_transaction_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: CarbonTransactionUpdate) -> Optional[CarbonTransaction]:
        db_obj = await carbon_transaction_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await carbon_transaction_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await carbon_transaction_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await carbon_transaction_repo.delete(db, id)
        return True