from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def new(session: AsyncSession, user: User):
    session.add(user)
    await session.commit()


async def get_all(session: AsyncSession):
    query = select(User)
    result = await session.scalars(query)
    return result.all()


async def get_one(session: AsyncSession, id: int | str):
    query = select(User).filter_by(id=id)
    result = await session.scalar(query)
    return result
