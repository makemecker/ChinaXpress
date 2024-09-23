from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

BUTTONS: dict[str, str] = {
    'buy': '🛒 Купить и доставить товар 🚚',
    'yes_url': '👍 Да, у меня есть ссылка 🔗',
    'no_url': '🚫 Нет, ссылки на товар не имеется.',
    'yes_description': '✅ Да, хочу ввести пояснение к заказу ✍️',
    'no_description': '❌ Нет, пояснение не нужно.',
    'yes_more_product': '✅ Да, я хочу заказать ещё один товар! 🛒',
    'no_more_product': '✅ Завершить заказ 📦',
    'alipay': '💸 Alipay',
    'wechat_pay': '💰 WeChat Pay',
    'other_bank': '🏦 Другой китайский банк',
    'yes_pay_description': '✅ Да, хочу ввести пояснение к оплате 💳✍️',
    'no_pay_description': '📩 Отправить заявку на оплату 💳',
    'pay': '💳 Оплатить товар 🛍️',
    'delivery': '🚚 Доставить товар 📦',
    'sizes': '📏 Длина, ширина, высота и масса коробки 📐',
    'volume': '📊 Объём и масса коробки📦',
    'density': '⚖️ Плотность 📦',
    'confirm_car_delivery': '✅ Да, доставка автотранспортом 🚗',
    'confirm_train_delivery': '✅ Да, доставка жд транспортом 🚂',
    'deny_delivery': '❌ Нет, не подтверждаю.',
    'yes_delivery_description': '✅ Да, хочу ввести пояснение к доставке 📦✍️',
    'no_delivery_description': '❌ Нет, пояснение не нужно.',
    'help': '🗣️ Обратиться к менеджеру 📞',
    }


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(*args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=BUTTONS[button] if button in BUTTONS else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
