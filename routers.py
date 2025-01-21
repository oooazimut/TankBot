from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram_dialog import DialogManager, StartMode
from apscheduler.schedulers.asyncio import asyncio

from db.repo import users
from service.modbus import create_modbus_client
from states import MainSG

start_router = Router()


@start_router.message(CommandStart())
async def start_nandler(msg: Message, dialog_manager: DialogManager):
    start_state = MainSG.passw
    user = await users.get_one(
        dialog_manager.middleware_data["session"],
        msg.from_user.id,
    )
    if user:
        start_state = MainSG.main
    await dialog_manager.start(state=start_state, mode=StartMode.RESET_STACK)


@start_router.callback_query(F.data == "reset_warning")
async def reset_warning(clb: CallbackQuery):
    async with await create_modbus_client() as client:
        await client.write_register(517, 1, slave=16)
        await asyncio.sleep(1)
        await client.write_register(517, 0, slave=16)

        await clb.answer("Звуковая сигнализация сброшена", show_alert=True)
        if clb.message and not isinstance(clb.message, InaccessibleMessage):
            await clb.message.delete()
