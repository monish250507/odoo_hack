
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.challenge import ChallengeCreate, ChallengeUpdate, ChallengeResponse
from services.challenge import ChallengeService

router = APIRouter(prefix="/challenges", tags=["Challenges"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[ChallengeResponse])
async def read_challenges(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await ChallengeService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(obj_in: ChallengeCreate, db: AsyncSession = Depends(get_db)):
    return await ChallengeService.create(db, obj_in)

@router.get("/{id}", response_model=ChallengeResponse)
async def read_challenge(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await ChallengeService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return item

@router.put("/{id}", response_model=ChallengeResponse)
async def update_challenge(id: uuid.UUID, obj_in: ChallengeUpdate, db: AsyncSession = Depends(get_db)):
    item = await ChallengeService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await ChallengeService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Challenge not found")