import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

import dialogs
import middlewares
import routers
from config import settings
from custom.media_storage import MediaIdStorage
from service.los import check_alarm, poll_registers


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    # logging.getLogger("apscheduler").setLevel(logging.WARNING)
    bot = Bot(settings.bot_token.get_secret_value())
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        poll_registers,
        trigger="interval",
        seconds=15,
        id="polling",
        kwargs={"bot": bot, "scheduler": scheduler},
    )
    scheduler.add_job(
        check_alarm,
        trigger="cron",
        hour=9,
        minute=0,
        kwargs={"bot": bot, "scheduler": scheduler},
    )
    storage = RedisStorage(
        Redis(), key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True)
    )
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(middlewares.DataMiddleware({"scheduler": scheduler}))
    dp.include_routers(routers.start_router, dialogs.main_dialog)
    setup_dialogs(dp, media_id_storage=MediaIdStorage())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
