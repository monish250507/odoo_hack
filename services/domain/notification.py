"""
Notification Service

Generates and persists in-app notifications for all system events.
This is a pure backend service — no AI calls.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession


class NotificationService:

    async def create_system_notification(
        self,
        db: AsyncSession,
        title: str,
        message: str,
        user_id: Optional[uuid.UUID] = None,
    ) -> dict:
        """
        Creates a system-wide or user-targeted notification.
        user_id=None means broadcast (not linked to specific user).
        """
        from repositories.notification import notification_repo

        record = await notification_repo.create(db, {
            "user_id": user_id,
            "title": title,
            "message": message,
            "is_read": False,
            "status": "active",
        })

        return {
            "notification_id": str(record.id),
            "title": title,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    async def mark_as_read(
        self,
        db: AsyncSession,
        notification_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> dict:
        from repositories.notification import notification_repo

        notif = await notification_repo.get_by_id(db, notification_id)
        if not notif:
            from core.exceptions import NotFoundException
            raise NotFoundException(f"Notification {notification_id} not found")

        await notification_repo.update(db, notif, {"is_read": True})
        return {"notification_id": str(notification_id), "is_read": True}

    async def get_user_notifications(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        unread_only: bool = False,
    ) -> list:
        from repositories.notification import notification_repo

        all_notifs = await notification_repo.get_all(db, skip=0, limit=200)
        user_notifs = [
            n for n in all_notifs
            if n.user_id is None or str(n.user_id) == str(user_id)
        ]

        if unread_only:
            user_notifs = [n for n in user_notifs if not n.is_read]

        return [
            {
                "id": str(n.id),
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in sorted(user_notifs, key=lambda x: x.created_at or datetime.min, reverse=True)
        ]


notification_service = NotificationService()
