from aiogram.fsm.state import StatesGroup, State


class BuyState(StatesGroup):
    check_url = State()
    check_count = State()
    check_photo = State()
    check_description = State()
    neutral = State()
