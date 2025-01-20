import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import dialogs
import middlewares
import routers
from config import settings
from custom.media_storage import MediaIdStorage
from service.los import check_alarm, poll_and_save


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    # logging.getLogger("apscheduler").setLevel(logging.WARNING)
    engine = create_async_engine(settings.sqlite_async_dsn, echo=False)
    db_pool = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(settings.bot_token.get_secret_value())
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        poll_and_save,
        trigger="interval",
        seconds=15,
        id="polling",
        args=[bot, db_pool],
    )
    scheduler.add_job(
        check_alarm,
        trigger="cron",
        hour=9,
        minute=0,
        args=[bot, db_pool],
    )
    storage = RedisStorage(
        Redis(), key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True)
    )
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(middlewares.APSchedulerMiddleware(scheduler))
    dp.update.outer_middleware(middlewares.DBSessionMiddleware(db_pool))
    dp.include_routers(routers.start_router, dialogs.main_dialog)
    setup_dialogs(dp, media_id_storage=MediaIdStorage())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
