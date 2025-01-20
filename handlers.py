import datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar

from config import settings
from db.models import User
from db.repo import los, users
from service.plot import PlotService
from states import MainSG


async def check_passwd(msg: Message, msg_inpt, manager: DialogManager):
    if msg.text == settings.passwd.get_secret_value():
        await users.new(
            manager.middleware_data["session"],
            User(id=msg.from_user.id, username=msg.from_user.full_name),
        )
        await manager.next()
    else:
        await msg.answer("Неверно, попробуйте ещё раз")


async def on_current_level(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    last_level = await los.get_last(manager.middleware_data["session"])
    if not last_level:
        await callback.answer("Данных нет.", show_alert=True)
        return

    if (
        last_level.level < settings.tank.low_border
        or last_level.level > settings.tank.high_border
    ):
        await callback.answer("Датчик неисправен!", show_alert=True)
        return

    curr_time = datetime.datetime.now()
    if last_level.timestamp >= curr_time - datetime.timedelta(minutes=2):
        PlotService.current_level(last_level.level)
        await manager.switch_to(MainSG.curr_level)
    else:
        await callback.answer("Данные устарели.", show_alert=True)


async def on_date_clicked(
    callback: CallbackQuery,
    widget: ManagedCalendar,
    manager: DialogManager,
    clicked_date: datetime.date,
    /,
):
    data = await los.get_by_date(manager.middleware_data["sesson"], clicked_date)
    if data:
        PlotService.archive_levels(data)
        await manager.switch_to(MainSG.archive)
    else:
        await callback.answer(f"Нет данных за {clicked_date}", show_alert=True)
