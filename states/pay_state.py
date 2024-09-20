from aiogram.fsm.state import StatesGroup, State


class PayState(StatesGroup):
    check_url = State()
    check_count = State()
    check_description = State()
