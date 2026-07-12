import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class EmissionFactor(FullBaseModel):
    __tablename__ = "emission_factors"
    __table_args__ = (Index("ix_ef_category_id", "category_id"),)

    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    factor_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(100), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
