from aiogram.fsm.state import StatesGroup, State


class DeliveryState(StatesGroup):
    check_dims = State()
    check_volume = State()
    check_density = State()
    check_weight = State()
    check_box_count = State()
    check_description = State()

