import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class PolicyAcknowledgement(FullBaseModel):
    __tablename__ = "policy_acknowledgements"
    __table_args__ = (
        Index("ix_pa_user_id", "user_id"),
        Index("ix_pa_policy_id", "policy_id"),
    )

    policy_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
