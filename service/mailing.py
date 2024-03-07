from aiogram import Bot


class Mailing:
    @staticmethod
    async def send_message(message: str, users: list, bot: Bot):
        for user in users:
            await bot.send_message(chat_id=user['id'], text=message)
