
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import async_session_maker
from schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from services.notification import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/", response_model=List[NotificationResponse])
async def read_notifications(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await NotificationService.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(obj_in: NotificationCreate, db: AsyncSession = Depends(get_db)):
    return await NotificationService.create(db, obj_in)

@router.get("/{id}", response_model=NotificationResponse)
async def read_notification(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await NotificationService.get_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    return item

@router.put("/{id}", response_model=NotificationResponse)
async def update_notification(id: uuid.UUID, obj_in: NotificationUpdate, db: AsyncSession = Depends(get_db)):
    item = await NotificationService.update(db, id, obj_in)
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    return item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    success = await NotificationService.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")