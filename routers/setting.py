
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.setting import SettingCreate, SettingUpdate, SettingResponse
from services.setting import SettingService

router = APIRouter(prefix="/settings", tags=["Settings"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[SettingResponse])
async def read_settings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await SettingService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=SettingResponse, status_code=status.HTTP_201_CREATED)
async def create_setting(obj_in: SettingCreate, db: AsyncSession = Depends(get_db)):
    return await SettingService.create(db, obj_in)

@router.get("/{id}", response_model=SettingResponse)
async def read_setting(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await SettingService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Setting not found")
    return item

@router.put("/{id}", response_model=SettingResponse)
async def update_setting(id: uuid.UUID, obj_in: SettingUpdate, db: AsyncSession = Depends(get_db)):
    item = await SettingService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Setting not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await SettingService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Setting not found")