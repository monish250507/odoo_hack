import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Index
from sqlalchemy import Uuid as UUID
from models.base import FullBaseModel

class ChallengeParticipation(FullBaseModel):
    __tablename__ = "challenge_participations"
    __table_args__ = (
        Index("ix_cp_user_id", "user_id"),
        Index("ix_cp_challenge_id", "challenge_id"),
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    challenge_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
