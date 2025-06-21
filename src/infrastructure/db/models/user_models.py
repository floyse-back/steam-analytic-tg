from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Integer, ForeignKey, Table, Column, String

from src.infrastructure.db.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

users_to_whishlist = Table(
    "users_to_whishlist",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("game_id", Integer, ForeignKey("whishlist.game_id"), primary_key=True)
)


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    steam_id: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)

    subscribes: Mapped[List["Subscribes"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    whishlist: Mapped[List[Whishlist]] = relationship(
        secondary=users_to_whishlist,
        back_populates="users"
    )


class Whishlist(Base):
    __tablename__ = 'whishlist'

    game_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    short_desc: Mapped[Optional[str]] = mapped_column(String,default="")
    price: Mapped[int] = mapped_column(Integer)

    users: Mapped[List[Users]] = relationship(
        secondary=users_to_whishlist,
        back_populates="whishlist"
    )


