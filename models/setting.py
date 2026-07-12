from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Index
from models.base import FullBaseModel

class Setting(FullBaseModel):
    __tablename__ = "settings"
    __table_args__ = (Index("ix_settings_key", "key", unique=True),)

    key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
