from datetime import datetime
from typing import Annotated

from sqlalchemy import REAL, TIMESTAMP, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


dttm = Annotated[
    datetime,
    mapped_column(TIMESTAMP, default=datetime.now, nullable=True),
]
classic_id = Annotated[
    int,
    mapped_column(primary_key=True, autoincrement=True, nullable=True),
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    username: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r})"


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[classic_id]
    level: Mapped[float] = mapped_column(REAL, nullable=True)
    timestamp: Mapped[dttm]

    def __repr__(self) -> str:
        return (
            f"Level(id={self.id!r}, level={self.level!r}, timestamp={self.timestamp!r})"
        )
