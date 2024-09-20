from keyboards.kb_generator import create_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from lexicon import LEXICON, ORDER


async def handle_order_process(message: Message, state: FSMContext):
    markup = create_inline_kb('yes_more_product', 'no_more_product')
    await message.answer(LEXICON['order_process'], reply_markup=markup)


async def handle_complete_pay(update: Message | CallbackQuery, state: FSMContext, admins: list, bot: Bot):
    if isinstance(update, CallbackQuery):
        await update.message.answer(LEXICON['complete_order'])
    else:
        await update.answer(LEXICON['complete_order'])

    for admin_id in admins:
        data = await state.get_data()
        order_message = await prepare_order(data,
                                            (update.from_user.username, update.from_user.id))
        await bot.send_message(admin_id, order_message)

    await state.clear()


async def prepare_order(data: dict, user_information: tuple[str | None, int]) -> str:
    message = ''
    for key, value in data.items():
        if key == 'photo':
            continue

        message += f'{ORDER.get(key)}: {value}\n'

    message += f'Имя пользователя: @{user_information[0]}\n'
    message += f'id пользователя: {user_information[1]}\n'

    return message
