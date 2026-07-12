
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.user import UserCreate, UserUpdate, UserResponse
from services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await UserService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(obj_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create(db, obj_in)

@router.get("/{id}", response_model=UserResponse)
async def read_user(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await UserService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item

@router.put("/{id}", response_model=UserResponse)
async def update_user(id: uuid.UUID, obj_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    item = await UserService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await UserService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")