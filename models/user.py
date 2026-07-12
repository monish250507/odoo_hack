import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class User(FullBaseModel):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_department_id", "department_id"),
        Index("ix_users_is_deleted", "is_deleted"),
    )

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(512), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="employee")  # admin | manager | employee
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
    points: Mapped[int] = mapped_column(default=0, server_default="0")
