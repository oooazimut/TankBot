from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

import config
from states import MainSG
from tools.plot import plot_service


async def check_passwd(msg: Message, msg_inpt, manager: DialogManager):
    if msg.text == config.PASSWD:
        await manager.next()
    else:
        await msg.answer('Неверно, попробуйте ещё раз')


main_dialog = Dialog(
    Window(
        Const('Введите пароль'),
        MessageInput(func=check_passwd, content_types=[ContentType.TEXT]),
        state=MainSG.passw
    ),
    Window(
        Const('Меню:'),
        Button(
            Const('Текущий уровень'),
            id='current_level',
            on_click=plot_service.show_current_level
        ),
        Button(
            Const('Архив изменений'),
            id='archive_levels',
            on_click=plot_service.show_archive_levels
        ),
        state=MainSG.main
    )
)
