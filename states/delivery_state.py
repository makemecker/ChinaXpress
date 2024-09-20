from aiogram.fsm.state import StatesGroup, State


class DeliveryState(StatesGroup):
    check_length = State()
    check_width = State()
    check_height = State()
    check_volume = State()
    check_density = State()
    check_box_count = State()
    check_description = State()

