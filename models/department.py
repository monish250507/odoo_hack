import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Index
from sqlalchemy import Uuid as UUID
from models.base import FullBaseModel

class Department(FullBaseModel):
    __tablename__ = "departments"
    __table_args__ = (
        Index("ix_departments_name", "name"),
        Index("ix_departments_is_deleted", "is_deleted"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
    code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
