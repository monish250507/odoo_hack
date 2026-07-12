"""
Notification Router — user notifications with read/unread state.
"""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_session_maker
from services.domain.notification import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/users/{user_id}")
async def get_user_notifications(
    user_id: uuid.UUID,
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    return await notification_service.get_user_notifications(db, user_id, unread_only)


@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    return await notification_service.mark_as_read(db, notification_id, user_id)
