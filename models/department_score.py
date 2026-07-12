import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Index
from sqlalchemy import Uuid as UUID
from models.base import FullBaseModel

class DepartmentScore(FullBaseModel):
    __tablename__ = "department_scores"
    __table_args__ = (Index("ix_ds_department_period", "department_id", "month", "year"),)

    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
