from aiogram.fsm.state import StatesGroup, State


class PayState(StatesGroup):
    wait_qr_code = State()
    wait_requisites = State()
    wait_amount = State()
    check_description = State()
