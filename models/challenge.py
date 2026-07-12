import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Integer, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class Challenge(FullBaseModel):
    __tablename__ = "challenges"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    goal: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
