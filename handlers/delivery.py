from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram import Router
from handlers.handler_functions import handle_order_process, handle_complete_pay
from lexicon import LEXICON
from keyboards.kb_generator import create_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from states.delivery_state import DeliveryState

# Инициализируем роутер уровня модуля
delivery_router: Router = Router()


@delivery_router.callback_query(F.data == 'delivery')
async def process_delivery(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(status='Доставка')
    markup = create_inline_kb('sizes', 'volume', 'density')
    await callback.message.answer(LEXICON['delivery_type'], reply_markup=markup)
    await callback.answer()


@delivery_router.callback_query(F.data == 'sizes')
async def process_delivery_sizes(callback: CallbackQuery, state: FSMContext):
    file_path = './images/box.jpg'
    photo = FSInputFile(file_path)
    await state.set_state(DeliveryState.check_length)
    await state.update_data(select_params='Длина, ширина и высота коробки')
    await callback.message.answer_photo(photo=photo, caption=LEXICON['delivery_request'])
    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_length))
async def process_length(message: Message, state: FSMContext):
    await state.update_data(length=message.text)
    await state.set_state(DeliveryState.check_width)
    await message.answer(LEXICON['width_request'])


@delivery_router.message(StateFilter(DeliveryState.check_width))
async def process_width(message: Message, state: FSMContext):
    await state.update_data(width=message.text)
    await state.set_state(DeliveryState.check_height)
    await message.answer(LEXICON['height_request'])


@delivery_router.message(StateFilter(DeliveryState.check_height))
async def process_width(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await state.set_state(DeliveryState.check_box_count)
    await message.answer(LEXICON['box_count_request'])


@delivery_router.callback_query(F.data == 'volume')
async def process_delivery_volume(callback: CallbackQuery, state: FSMContext):
    await state.update_data(select_params='Объём коробки')
    await state.set_state(DeliveryState.check_volume)
    await callback.message.answer(LEXICON['volume_request'])
    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_volume))
async def process_volume(message: Message, state: FSMContext):
    await state.update_data(volume=message.text)
    await state.set_state(DeliveryState.check_box_count)
    await message.answer(LEXICON['box_count_request'])


@delivery_router.callback_query(F.data == 'density')
async def process_delivery_volume(callback: CallbackQuery, state: FSMContext):
    await state.update_data(select_params='Плотность коробки')
    await state.set_state(DeliveryState.check_density)
    await callback.message.answer(LEXICON['density_request'])
    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_density))
async def process_volume(message: Message, state: FSMContext):
    await state.update_data(density=message.text)
    await state.set_state(DeliveryState.check_box_count)
    await message.answer(LEXICON['box_count_request'])


@delivery_router.message(StateFilter(DeliveryState.check_box_count))
async def process_box_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    markup = create_inline_kb('confirm_delivery', 'deny_delivery')
    await message.answer(LEXICON['delivery_price'], reply_markup=markup)


@delivery_router.callback_query(F.data == 'confirm_delivery')
async def delivery_confirmation(callback: CallbackQuery):
    markup = create_inline_kb('yes_delivery_description', 'no_delivery_description')
    await callback.message.answer(LEXICON['delivery_description_request'], reply_markup=markup)
    await callback.answer()


@delivery_router.callback_query(F.data == 'yes_delivery_description')
async def delivery_description(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_description='Имеется пояснение к оплате')
    await state.set_state(DeliveryState.check_description)
    await callback.message.answer(LEXICON['delivery_description_enter'])
    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_description))
async def process_delivery_description(message: Message, state: FSMContext, admins: list, bot: Bot):
    await state.update_data(description=message.text)
    await handle_complete_pay(message, state, admins, bot)


@delivery_router.callback_query(F.data == 'no_delivery_description')
async def process_no_delivery_description(callback: CallbackQuery, state: FSMContext, admins: list, bot: Bot):
    await state.update_data(is_description='Пояснения к оплате нет')
    await handle_complete_pay(callback, state, admins, bot)
    await callback.answer()
