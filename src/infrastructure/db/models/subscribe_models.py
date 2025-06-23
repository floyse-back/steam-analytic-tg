from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.database import Base


class Subscribes(Base):
    __tablename__ = "subscribes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("subscribes_types.id"), nullable=False)
    role_permitions: Mapped[int] = mapped_column(Integer, nullable=1)

    user: Mapped["Users"] = relationship(back_populates="subscribes")
    type: Mapped[SubscribesType] = relationship(back_populates="subscribes")

    subscribes_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


class SubscribesType(Base):
    __tablename__ = "subscribes_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    subscribes: Mapped[List[Subscribes]] = relationship(
        back_populates="type",
        cascade="all, delete-orphan"
    )
