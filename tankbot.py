import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

import config
import dialogs
import routers
from custom.media_storage import MediaIdStorage
from functions import regs_polling


async def on_startup():
    asyncio.create_task(regs_polling())

async def main():
    bot = Bot(config.TOKEN)
    storage = RedisStorage(Redis(), key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True))
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.include_routers(routers.start_router, dialogs.main_dialog)
    setup_dialogs(dp, media_id_storage=MediaIdStorage())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
