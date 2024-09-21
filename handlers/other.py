from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from lexicon import LEXICON
from aiogram import F

# Инициализируем роутер уровня модуля
other_router: Router = Router()


@other_router.message(Command(commands=['help']))
@other_router.callback_query(F.data == 'help')
async def help_command(update: Message | CallbackQuery):
    if isinstance(update, CallbackQuery):
        await update.answer()
        update = update.message
    await update.answer(LEXICON['/help'])


@other_router.message()
async def any_unmark_message(message: Message):
    await message.answer(LEXICON['other'])
