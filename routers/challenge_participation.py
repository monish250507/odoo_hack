
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.challenge_participation import ChallengeParticipationCreate, ChallengeParticipationUpdate, ChallengeParticipationResponse
from services.challenge_participation import ChallengeParticipationService

router = APIRouter(prefix="/challenge_participations", tags=["ChallengeParticipations"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[ChallengeParticipationResponse])
async def read_challenge_participations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await ChallengeParticipationService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=ChallengeParticipationResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge_participation(obj_in: ChallengeParticipationCreate, db: AsyncSession = Depends(get_db)):
    return await ChallengeParticipationService.create(db, obj_in)

@router.get("/{id}", response_model=ChallengeParticipationResponse)
async def read_challenge_participation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await ChallengeParticipationService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="ChallengeParticipation not found")
    return item

@router.put("/{id}", response_model=ChallengeParticipationResponse)
async def update_challenge_participation(id: uuid.UUID, obj_in: ChallengeParticipationUpdate, db: AsyncSession = Depends(get_db)):
    item = await ChallengeParticipationService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="ChallengeParticipation not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge_participation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await ChallengeParticipationService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="ChallengeParticipation not found")