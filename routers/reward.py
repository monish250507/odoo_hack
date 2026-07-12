
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.reward import RewardCreate, RewardUpdate, RewardResponse
from services.reward import RewardService

router = APIRouter(prefix="/rewards", tags=["Rewards"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[RewardResponse])
async def read_rewards(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await RewardService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=RewardResponse, status_code=status.HTTP_201_CREATED)
async def create_reward(obj_in: RewardCreate, db: AsyncSession = Depends(get_db)):
    return await RewardService.create(db, obj_in)

@router.get("/{id}", response_model=RewardResponse)
async def read_reward(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await RewardService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Reward not found")
    return item

@router.put("/{id}", response_model=RewardResponse)
async def update_reward(id: uuid.UUID, obj_in: RewardUpdate, db: AsyncSession = Depends(get_db)):
    item = await RewardService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Reward not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reward(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await RewardService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Reward not found")