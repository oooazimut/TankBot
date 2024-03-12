from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Mailing:
    @staticmethod
    async def send_message(message: str, users: list, bot: Bot):
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text='Сброс', callback_data='reset_warning'))
        for user in users:
            await bot.send_message(chat_id=user['id'], text=message, reply_markup=builder.as_markup())
