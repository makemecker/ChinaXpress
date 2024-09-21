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
    markup = create_inline_kb('alipay', 'wechat_pay', 'other_bank')
    await callback.message.answer(LEXICON['about_pay'], reply_markup=markup)
    await callback.answer()


@pay_router.callback_query(F.data.in_(['alipay', 'wechat_pay']))
async def alipay_or_wechat_pay(callback: CallbackQuery, state: FSMContext):
    await state.update_data(bank='Alipay' if callback.data == 'alipay' else 'wechat_pay')
    await callback.message.answer(LEXICON['qr_code'])
    await state.set_state(PayState.wait_qr_code)
    await callback.answer()


@pay_router.callback_query(F.data == 'other_bank')
async def other_bank(callback: CallbackQuery, state: FSMContext):
    await state.update_data(bank='Другой китайский банк')
    await callback.message.answer(LEXICON['other_bank'])
    await state.set_state(PayState.wait_requisites)
    await callback.answer()


@pay_router.message(StateFilter(PayState.wait_requisites))
async def qr_code(message: Message, state: FSMContext):
    # Проверяем, если ли в сообщении фотографии
    if message.photo:
        # Получаем максимальное качество фото (последний элемент в списке)
        photo = message.photo[-1].file_id

        # Получаем текущий список фотографий из состояния
        state_data = await state.get_data()
        photos = state_data.get('photo', [])

        # Добавляем новый файл в список фотографий
        photos.append(photo)

        # Обновляем данные в состоянии
        await state.update_data(photo=photos)
        await state.update_data(is_photo='Имеются фотографии')
    # Если фотографии нет, сохраняем текстовые реквизиты
    else:
        await state.update_data(requisites=message.text)

    # Переход к следующему шагу
    await message.answer(LEXICON['amount'])
    await state.set_state(PayState.wait_amount)


@pay_router.message(StateFilter(PayState.wait_qr_code))
async def qr_code(message: Message, state: FSMContext):
    if message.photo:
        # Получаем максимальное качество фото (последний элемент в списке)
        photo = message.photo[-1]
        # Сохраняем file_id фото в data состояния
        await state.update_data(is_photo='Имеется фото')
        await state.update_data(photo=photo.file_id)
        await message.answer(LEXICON['amount'])
        await state.set_state(PayState.wait_amount)
    else:
        await message.answer(LEXICON['need_photo'])


@pay_router.message(StateFilter(PayState.wait_amount))
async def amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
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
