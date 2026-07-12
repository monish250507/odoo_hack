from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Index
from models.base import FullBaseModel

class Category(FullBaseModel):
    __tablename__ = "categories"
    __table_args__ = (Index("ix_categories_name", "name"),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # emission | activity | csr
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
