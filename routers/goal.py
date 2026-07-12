
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from services.goal import GoalService

router = APIRouter(prefix="/goals", tags=["Goals"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[GoalResponse])
async def read_goals(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await GoalService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(obj_in: GoalCreate, db: AsyncSession = Depends(get_db)):
    return await GoalService.create(db, obj_in)

@router.get("/{id}", response_model=GoalResponse)
async def read_goal(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await GoalService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Goal not found")
    return item

@router.put("/{id}", response_model=GoalResponse)
async def update_goal(id: uuid.UUID, obj_in: GoalUpdate, db: AsyncSession = Depends(get_db)):
    item = await GoalService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Goal not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await GoalService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")