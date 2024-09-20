from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram import Router
from handlers.handler_functions import handle_order_process, prepare_order
from lexicon import LEXICON
from keyboards.kb_generator import create_inline_kb
from aiogram.fsm.context import FSMContext

from states.buy_state import BuyState

# Инициализируем роутер уровня модуля
buy_router: Router = Router()


@buy_router.callback_query(F.data.in_(['buy', 'yes_more_product']))
async def process_buy(callback: CallbackQuery, state: FSMContext, admins: list, bot: Bot):
    markup = create_inline_kb('yes_url', 'no_url')
    await state.update_data(status='Покупка')
    await callback.message.answer(LEXICON['buy_type'], reply_markup=markup)

    if callback.data == 'yes_more_product':
        for admin_id in admins:
            data = await state.get_data()
            order_message = await prepare_order(data,
                                                (callback.from_user.username, callback.from_user.id))
            await bot.send_message(admin_id, order_message)
            if data.get('is_photo'):
                await bot.send_photo(admin_id, data['photo'])

    await state.clear()
    await callback.answer()


@buy_router.callback_query(F.data == 'yes_url')
async def process_yes_url(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON['url_request'])
    await state.update_data(is_url='Ссылка указана')
    await state.set_state(BuyState.check_url)
    await callback.answer()


@buy_router.callback_query(F.data == 'no_url')
async def process_no_url(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON['photo_request'])
    await state.update_data(is_url='Ссылка не указана')
    await state.set_state(BuyState.check_photo)
    await callback.answer()


@buy_router.message(StateFilter(BuyState.check_url, BuyState.check_photo))
async def process_url(message: Message, state: FSMContext):
    current_state = await state.get_state()

    # Проверяем, в каком из состояний находится пользователь
    if current_state == BuyState.check_url.state:
        await state.update_data(url=message.text)
    else:
        if message.photo:
            # Получаем максимальное качество фото (последний элемент в списке)
            photo = message.photo[-1]
            # Сохраняем file_id фото в data состояния
            await state.update_data(is_photo='Имеется фото')
            await state.update_data(photo=photo.file_id)

    await message.answer(LEXICON['count_request'])
    await state.set_state(BuyState.check_count)


@buy_router.message(StateFilter(BuyState.check_count))
async def process_count(message: Message, state: FSMContext):
    markup = create_inline_kb('yes_description', 'no_description')
    await state.update_data(count=message.text)
    await message.answer(LEXICON['description_request'], reply_markup=markup)

    await state.set_state(BuyState.neutral)


@buy_router.callback_query(F.data == 'yes_description')
async def process_yes_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyState.check_description)
    await state.update_data(is_description='Есть пояснение')
    await callback.message.answer(LEXICON['description_enter'])
    await callback.answer()


@buy_router.message(StateFilter(BuyState.check_description))
async def process_description_enter(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await handle_order_process(message, state)


@buy_router.callback_query(F.data == 'no_description')
async def process_no_description(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_description='Пояснения нет')
    await handle_order_process(callback.message, state)
    await callback.answer()


@buy_router.callback_query(F.data == 'no_more_product')
async def complete_order(callback: CallbackQuery, state: FSMContext, bot: Bot, admins: list):
    await callback.message.answer(LEXICON['complete_order'])
    await callback.answer()

    for admin_id in admins:
        data = await state.get_data()
        order_message = await prepare_order(data,
                                            (callback.from_user.username, callback.from_user.id))
        await bot.send_message(admin_id, order_message)
        if data.get('is_photo'):
            await bot.send_photo(admin_id, data['photo'])

    await state.clear()
