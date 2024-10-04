from typing import Any

from database import DatabaseManager
from keyboards.kb_generator import create_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from lexicon import LEXICON, ORDER
import re


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
        if data.get('is_photo'):
            photo = data['photo']
            if isinstance(photo, list):
                for cur_photo in photo:
                    await bot.send_photo(admin_id, cur_photo)
            else:
                await bot.send_photo(admin_id, photo)

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


async def is_valid_number(s):
    # Регулярное выражение для проверки числа (целое или дробное)
    s = s.strip()
    pattern = r'^\d+(\.\d+)?$'
    return bool(re.match(pattern, s))


async def is_valid_dimensions(s: str) -> bool:
    # Удаляем пробелы в начале и конце строки
    s = s.strip()
    # Регулярное выражение для формата: числоxчислоxчисло, где x может быть русской "х" или английской "x"
    pattern = r'^\d+\s*[хx]\s*\d+\s*[хx]\s*\d+$'
    return bool(re.match(pattern, s))


async def parse_dimensions(s: str) -> tuple:
    # Удаляем пробелы в начале и конце строки
    s = s.strip()
    # Заменяем русскую "х" на английскую "x" для единообразия
    s = s.replace('х', 'x').replace('Х', 'x')
    # Разделяем строку по символу "x"
    length, width, height = s.split('x')
    # Приводим значения к числовому формату
    return float(length.strip()), float(width.strip()), float(height.strip())


async def calc_price(data: dict[str, str], database: DatabaseManager) -> tuple[float, float]:
    volume = data.get('volume', False)
    if not volume:
        volume = 1
        for dim in ['length', 'width', 'height']:
            volume *= float(data[dim]) * 0.01
    weight = float(data['weight'])
    volume = float(volume)
    density = round(weight / volume if volume != 0 else 0)

    query = '''
    SELECT car, train
    FROM delivery_price
    WHERE density_min <= ? AND density_max >= ?;
    '''

    # Выполняем запрос, передавая значение плотности
    result = database.fetchone(query, (density, density))

    if result is None:
        logging.warning(f"No pricing information found for density {density}.")
        return 0, 0

    car_price, train_price = result

    car_price *= volume if density <= 100 else weight
    train_price *= volume if density <= 100 else weight

    if "length" in data:
        car_price *= float(data['count'])
        train_price *= float(data['count'])

    return round(car_price, 2), round(train_price, 2)


async def process_price(data: dict[str, Any], database: DatabaseManager, message: Message) -> dict[str, str] | None:
    car_price, train_price = await calc_price(data, database)
    if car_price:
        markup = create_inline_kb('confirm_car_delivery', 'confirm_train_delivery', 'deny_delivery')
        await message.answer(LEXICON['delivery_price'].format(car_price, train_price), reply_markup=markup)
        data["car_price"] = car_price
        data["train_price"] = train_price
    else:
        return None

    return data


async def update_price_and_state(data: dict, state: FSMContext, database: DatabaseManager, message: Message):
    price_data = await process_price(data, database, message)
    if price_data:
        await state.update_data(price_data)
    else:
        await message.answer(LEXICON['cant_calc_price'])
        await state.clear()
