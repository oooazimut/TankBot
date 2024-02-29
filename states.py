from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    passw = State()
    main = State()