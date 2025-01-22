from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Level


async def get_by_date(session: AsyncSession, curr_date: date):
    query = select(Level).where(func.date(Level.timestamp) == curr_date.isoformat())
    result = await session.scalars(query)
    return result.all()


async def get_last(session: AsyncSession):
    query = select(Level).order_by(Level.id.desc()).limit(1)
    result = await session.scalar(query)
    return result


async def new(session: AsyncSession, level: Level):
    session.add(level)
    await session.commit()
