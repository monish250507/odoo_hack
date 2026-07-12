from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Integer
from models.base import FullBaseModel

class Reward(FullBaseModel):
    __tablename__ = "rewards"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cost: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")
    stock: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active")
