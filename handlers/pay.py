from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram import Router
from handlers.handler_functions import handle_order_process, handle_complete_pay
from lexicon import LEXICON
from keyboards.kb_generator import create_inline_kb
from aiogram.fsm.context import FSMContext

from states.pay_state import PayState

# Инициализируем роутер уровня модуля
pay_router: Router = Router()


@pay_router.callback_query(F.data == 'pay')
async def pay_url_request(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(status='Оплата')
    await callback.message.answer(LEXICON['url_request'])
    await state.set_state(PayState.check_url)
    await callback.answer()


@pay_router.message(StateFilter(PayState.check_url))
async def pay_count_request(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(LEXICON['count_request'])
    await state.set_state(PayState.check_count)


@pay_router.message(StateFilter(PayState.check_count))
async def process_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    markup = create_inline_kb('yes_pay_description', 'no_pay_description')
    await message.answer(LEXICON['description_pay_request'], reply_markup=markup)


@pay_router.callback_query(F.data == 'yes_pay_description')
async def process_yes_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PayState.check_description)
    await state.update_data(is_description='Есть пояснение к оплате')
    await callback.message.answer(LEXICON['description_pay_enter'])
    await callback.answer()


@pay_router.message(StateFilter(PayState.check_description))
async def process_description_enter(message: Message, state: FSMContext, admins: list, bot: Bot):
    await state.update_data(description=message.text)
    await handle_complete_pay(message, state, admins, bot)


@pay_router.callback_query(F.data == 'no_pay_description')
async def process_no_description(callback: CallbackQuery, state: FSMContext, admins: list, bot: Bot):
    await handle_complete_pay(callback, state, admins, bot)
    await callback.answer()
