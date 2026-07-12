import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class EmployeeParticipation(FullBaseModel):
    __tablename__ = "employee_participations"
    __table_args__ = (
        Index("ix_ep_user_id", "user_id"),
        Index("ix_ep_activity_id", "activity_id"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    activity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    hours: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending")
