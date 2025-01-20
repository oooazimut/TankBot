from datetime import date 
from apscheduler.schedulers.asyncio import asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import settings
from db.models import Level


engine = create_async_engine(settings.sqlite_async_dsn, echo=False)
db_pool = async_sessionmaker(engine, expire_on_commit=False)

async def main():
    curr_date = date.today()
    async with db_pool() as session:
        query = select(Level).where(func.date(Level.timestamp) == curr_date.isoformat())
        data = await session.scalars(query)
        print(data.all())

asyncio.run(main())
