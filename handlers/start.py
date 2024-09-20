from aiogram.types import Message, InputFile, FSInputFile
from aiogram.filters import Command
from keyboards.kb_generator import create_inline_kb
from aiogram import Router
from lexicon import LEXICON

# Инициализируем роутер уровня модуля
start_router: Router = Router()


@start_router.message(Command('start'))
async def user_start(update: Message):
    # Загружаем изображение (предположим, что оно находится в папке проекта)
    file_path = './images/start.jpg'
    photo = FSInputFile(file_path)
    # Создаем клавиатуру
    markup = create_inline_kb('buy', 'pay', 'delivery')
    await update.answer_photo(photo=photo, caption=LEXICON['/start'], reply_markup=markup)
