from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    passw = State()
    main = State()
    curr_level = State()
    archive = State()
    calendar = State()
