from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import  Message
from aiogram_dialog import DialogManager, StartMode


start_router = Router()

@start_router.message(CommandStart())
async def start_nandler(msg: Message, manager: DialogManager):
    print(msg.from_user.id)