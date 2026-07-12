import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy import Uuid as UUID
from models.base import FullBaseModel

class Audit(FullBaseModel):
    __tablename__ = "audits"
    __table_args__ = (Index("ix_audit_department_id", "department_id"),)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    auditor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending")
