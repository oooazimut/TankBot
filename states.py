from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    passw = State()
    main = State()
    curr_level = State()
    archive = State()
    calendar = State()
