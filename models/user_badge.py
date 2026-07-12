import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class UserBadge(FullBaseModel):
    __tablename__ = "user_badges"
    __table_args__ = (Index("ix_ub_user_id", "user_id"),)

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    badge_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    awarded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
