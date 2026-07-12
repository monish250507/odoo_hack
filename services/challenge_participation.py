
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.challenge_participation import challenge_participation_repo
from schemas.challenge_participation import ChallengeParticipationCreate, ChallengeParticipationUpdate
from models.challenge_participation import ChallengeParticipation

class ChallengeParticipationService:
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ChallengeParticipation]:
        return await challenge_participation_repo.get_all(db, skip=skip, limit=limit)

    @staticmethod
    async def get_by_id(db: AsyncSession, id: uuid.UUID) -> Optional[ChallengeParticipation]:
        return await challenge_participation_repo.get_by_id(db, id)

    @staticmethod
    async def create(db: AsyncSession, obj_in: ChallengeParticipationCreate) -> ChallengeParticipation:
        return await challenge_participation_repo.create(db, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def update(db: AsyncSession, id: uuid.UUID, obj_in: ChallengeParticipationUpdate) -> Optional[ChallengeParticipation]:
        db_obj = await challenge_participation_repo.get_by_id(db, id)
        if not db_obj:
            return None
        return await challenge_participation_repo.update(db, db_obj, obj_in.model_dump(exclude_unset=True))

    @staticmethod
    async def delete(db: AsyncSession, id: uuid.UUID) -> bool:
        db_obj = await challenge_participation_repo.get_by_id(db, id)
        if not db_obj:
            return False
        await challenge_participation_repo.delete(db, id)
        return True