import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.repo import users as users_repo
from config import settings

logger = logging.getLogger(__name__)


async def send_message(message: str, session: AsyncSession, bot: Bot):
    users = await users_repo.get_all(session)
    builder = InlineKeyboardBuilder()
    if not message == settings.alarms.POSSIBLY_LACK_OF_POWER:
        builder.add(InlineKeyboardButton(text="Сброс", callback_data="reset_warning"))

    for user in users:
        try:
            await bot.send_message(
                chat_id=user.id,
                text=message,
                reply_markup=builder.as_markup(),
            )
        except TelegramBadRequest:
            pass
        except TelegramForbiddenError as errr:
            logger.error(f"{message}:\nОшибка отправки: {str(errr)}")
