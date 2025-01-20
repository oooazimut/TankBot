from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.repo import users as users_repo


async def send_message(message: str, session: AsyncSession, bot: Bot):
    users = await users_repo.get_all(session)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Сброс", callback_data="reset_warning"))

    for user in users:
        await bot.send_message(
            chat_id=user.id,
            text=message,
            reply_markup=builder.as_markup(),
        )
