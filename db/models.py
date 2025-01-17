from datetime import datetime
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


dttm = Annotated[datetime, mapped_column(default=datetime.now)]
classic_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r})"


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[classic_id]
    level: Mapped[float]
    timestamp: Mapped[dttm]

    def __repr__(self) -> str:
        return (
            f"Level(id={self.id!r}, level={self.level!r}, timestamp={self.timestamp!r})"
        )
