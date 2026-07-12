import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text, Index
from sqlalchemy import Uuid as UUID
from models.base import FullBaseModel

class CarbonTransaction(FullBaseModel):
    __tablename__ = "carbon_transactions"
    __table_args__ = (
        Index("ix_ct_user_id", "user_id"),
        Index("ix_ct_type", "type"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # credit | debit
    source: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
