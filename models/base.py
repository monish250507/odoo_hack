import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, Integer
from sqlalchemy.sql import func
from sqlalchemy import Uuid as UUID


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    """
    Abstract base model that includes id, created_at, and updated_at fields.
    """
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FullBaseModel(BaseModel):
    """
    Abstract base model that includes soft deletes, optimistic locking, and audit tracking.
    Compatible with Python 3.9+ (uses Optional instead of X | None syntax).
    """
    __abstract__ = True

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, server_default='1')

    # Audit tracking — UUID columns (no FK to avoid circular dependency)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

    __mapper_args__ = {
        "version_id_col": version,
    }
