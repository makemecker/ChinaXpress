from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram import Router

from database import DatabaseManager
from handlers.handler_functions import is_valid_number, handle_complete_pay, calc_price, is_valid_dimensions, \
    parse_dimensions
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
    markup = create_inline_kb('sizes', 'volume')
    await callback.message.answer(LEXICON['delivery_type'], reply_markup=markup)
    await callback.answer()


@delivery_router.callback_query(F.data == 'sizes')
async def process_delivery_sizes(callback: CallbackQuery, state: FSMContext):
    file_path = './images/box.jpg'
    photo = FSInputFile(file_path)
    await state.set_state(DeliveryState.check_dims)
    await state.update_data(select_params='Длина, ширина и высота коробки')
    await callback.message.answer_photo(photo=photo, caption=LEXICON['length_request'])

    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_dims))
async def process_dims(message: Message, state: FSMContext):
    if await is_valid_dimensions(message.text):
        length, width, height = await parse_dimensions(message.text)

        await state.update_data(length=length)
        await state.update_data(width=width)
        await state.update_data(height=height)

        await message.answer(LEXICON['weight_request'])
        await state.set_state(DeliveryState.check_weight)
    else:
        await message.answer(LEXICON['need_dim_format'])


@delivery_router.callback_query(F.data == 'volume')
async def process_delivery_volume(callback: CallbackQuery, state: FSMContext):
    await state.update_data(select_params='Объём коробки')
    await state.set_state(DeliveryState.check_volume)
    await callback.message.answer(LEXICON['volume_request'])
    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_volume))
async def process_volume(message: Message, state: FSMContext):
    if await is_valid_number(message.text):
        await state.update_data(volume=message.text)
        await state.set_state(DeliveryState.check_weight)
        await message.answer(LEXICON['weight_request'])
    else:
        await message.answer(LEXICON['need_number'])


@delivery_router.callback_query(F.data == 'density')
async def process_delivery_volume(callback: CallbackQuery, state: FSMContext):
    await state.update_data(select_params='Плотность коробки')
    await state.set_state(DeliveryState.check_density)
    await callback.message.answer(LEXICON['density_request'])
    await callback.answer()


@delivery_router.message(StateFilter(DeliveryState.check_density))
async def process_volume(message: Message, state: FSMContext):
    if await is_valid_number(message.text):

        await state.update_data(density=message.text)
        await state.set_state(DeliveryState.check_weight)
        await message.answer(LEXICON['weight_request'])

    else:
        await message.answer(LEXICON['need_number'])


@delivery_router.message(StateFilter(DeliveryState.check_weight))
async def process_weight(message: Message, state: FSMContext):
    message_text = message.text
    if await is_valid_number(message_text):
        await state.update_data(weight=message_text)

        await state.set_state(DeliveryState.check_box_count)
        await message.answer(LEXICON['box_count_request'])
    else:
        await message.answer(LEXICON['need_number'])


@delivery_router.message(StateFilter(DeliveryState.check_box_count))
async def process_box_count(message: Message, state: FSMContext, database: DatabaseManager):
    if await is_valid_number(message.text):

        await state.update_data(count=message.text)
        car_price, train_price = await calc_price(await state.get_data(), database)
        print(2)
        markup = create_inline_kb('confirm_car_delivery', 'confirm_train_delivery', 'deny_delivery')
        await message.answer(LEXICON['delivery_price'].format(car_price, train_price), reply_markup=markup)
        await state.update_data(car_price=car_price)
        await state.update_data(train_price=train_price)
    else:
        await message.answer(LEXICON['need_number'])


@delivery_router.callback_query(F.data == 'confirm_car_delivery')
async def delivery_confirmation(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery_type='Автотранспорт')
    markup = create_inline_kb('yes_delivery_description', 'no_delivery_description')
    await callback.message.answer(LEXICON['delivery_description_request'], reply_markup=markup)
    await callback.answer()


@delivery_router.callback_query(F.data == 'confirm_train_delivery')
async def delivery_confirmation(callback: CallbackQuery, state: FSMContext):
    await state.update_data(delivery_type='Жд транспорт')
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
