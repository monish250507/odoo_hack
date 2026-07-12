import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Goal(FullBaseModel):
    __tablename__ = "goals"
    __table_args__ = (Index("ix_goals_department_id", "department_id"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    unit: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="on_track", server_default="on_track")
