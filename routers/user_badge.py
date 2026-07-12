
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.user_badge import UserBadgeCreate, UserBadgeUpdate, UserBadgeResponse
from services.user_badge import UserBadgeService

router = APIRouter(prefix="/user_badges", tags=["UserBadges"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[UserBadgeResponse])
async def read_user_badges(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await UserBadgeService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=UserBadgeResponse, status_code=status.HTTP_201_CREATED)
async def create_user_badge(obj_in: UserBadgeCreate, db: AsyncSession = Depends(get_db)):
    return await UserBadgeService.create(db, obj_in)

@router.get("/{id}", response_model=UserBadgeResponse)
async def read_user_badge(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await UserBadgeService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="UserBadge not found")
    return item

@router.put("/{id}", response_model=UserBadgeResponse)
async def update_user_badge(id: uuid.UUID, obj_in: UserBadgeUpdate, db: AsyncSession = Depends(get_db)):
    item = await UserBadgeService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="UserBadge not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_badge(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await UserBadgeService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="UserBadge not found")