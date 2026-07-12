import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Text, Index
from sqlalchemy import Uuid as UUID
from models.base import FullBaseModel

class ProductESGProfile(FullBaseModel):
    __tablename__ = "product_esg_profiles"
    __table_args__ = (Index("ix_pep_department_id", "department_id"),)

    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    carbon_footprint: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    energy_usage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    water_usage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
