from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

import handlers
from custom.babel_calendar import CustomCalendar
from states import MainSG

main_dialog = Dialog(
    Window(
        Const('Введите пароль'),
        MessageInput(func=handlers.check_passwd, content_types=[ContentType.TEXT]),
        state=MainSG.passw
    ),
    Window(
        Const('Меню:'),
        Button(
            Const('Текущий уровень'),
            id='current_level',
            on_click=handlers.on_current_level
        ),
        SwitchTo(
            Const('Архив изменений'),
            id='to_calendar',
            state=MainSG.calendar
        ),
        state=MainSG.main
    ),
    Window(
        Const('Текущий уровень:'),
        SwitchTo(Const('Назад'), id='to_main', state=MainSG.main),
        StaticMedia(path='curr_level.png', type=ContentType.PHOTO),
        state=MainSG.curr_level,
    ),
    Window(
        Const('Выберите дату:'),
        CustomCalendar(id='cal', on_click=handlers.on_date_clicked),
        SwitchTo(Const('Назад'), id='to_main', state=MainSG.main),
        state=MainSG.calendar
    )
)
