from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from db.repo import UserRepo as UsSrv
from states import MainSG

start_router = Router()


@start_router.message(CommandStart())
async def start_nandler(msg: Message, dialog_manager: DialogManager):
    start_state = MainSG.passw

    user = UsSrv.get_user_by_id(msg.from_user.id)
    if user:
        start_state = MainSG.main

    await dialog_manager.start(state=start_state, mode=StartMode.RESET_STACK)
