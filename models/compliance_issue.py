import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from models.base import FullBaseModel

class ComplianceIssue(FullBaseModel):
    __tablename__ = "compliance_issues"
    __table_args__ = (Index("ix_ci_audit_id", "audit_id"),)

    audit_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(50), default="medium")  # low | medium | high | critical
    status: Mapped[str] = mapped_column(String(50), default="open", server_default="open")
