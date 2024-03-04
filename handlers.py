import datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar

import config
from db.service import UserService, LosService
from states import MainSG
from tools.plot import PlotService


async def check_passwd(msg: Message, msg_inpt, manager: DialogManager):
    if msg.text == config.PASSWD:
        UserService.add_user(msg.from_user.id, msg.from_user.full_name)
        await manager.next()
    else:
        await msg.answer('Неверно, попробуйте ещё раз')


async def on_current_level(callback: CallbackQuery, button: Button, manager: DialogManager):
    last_level = LosService.get_last_level()
    if last_level:
        last_level = last_level[0]
        curr_time = datetime.datetime.now().replace(second=0, microsecond=0)
        if last_level['timestamp'].replace(second=0) == curr_time:
            PlotService.current_level()
            await manager.switch_to(MainSG.curr_level)
        else:
            await callback.answer('Данные устарели.')
    else:
        await callback.answer('Данных нет.')


async def on_archive_levels(callback: CallbackQuery, button: Button, manager: DialogManager):
    return None


async def on_date_clicked(callback: ChatEvent, widget: ManagedCalendar, manager: DialogManager, clicked_date: datetime.date, /):
    await callback.answer(str(clicked_date))
