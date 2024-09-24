from config import load_config

LEXICON: dict[str, str] = {
    'buy_type': '😊 Подскажите, пожалуйста, есть ли у вас ссылка на интересующий Вас товар? 🔗',
    'url_request': '🔗 Пришлите, пожалуйста, ссылку на интересующий вас товар. Спасибо! 😊',
    'count_request': '🔢 Введите, пожалуйста, необходимое количество выбранного товара. Пример: 55',
    'photo_request': '📸 Пришлите, пожалуйста, изображение необходимого товара. Спасибо! 😊',
    'description_request': '💬 Отлично! Хотите ли Вы добавить какое-либо пояснение к заказу (дополнительные '
                           'характеристики товара и т.д.)? 😊',
    'description_enter': '😊 Пожалуйста, введите пояснение к вашему заказу. Мы хотим сделать всё как можно лучше! 💬',
    'about_pay': '💳 Мы можем оплатить счета через платёжные системы Alipay, WeChat Pay, а также другие китайские '
                 'банки. 🇨🇳 \n\n🔍 Выберите, пожалуйста, счёт какой платёжной системы или банка Вы хотели бы оплатить. '
                 '😊',
    'qr_code': '📱 Пришлите, пожалуйста, QR-код счёта для оплаты в виде фотографии или скриншота. Спасибо! 😊',
    'other_bank': '📄 Пришлите, пожалуйста, полные реквизиты счёта для оплаты в текстовом виде, либо в виде '
                  'фотографии или скриншота. 📸',
    'need_photo': '📸 Пришлите, пожалуйста, фотографию или скриншот. Для отмены наберите команду /menu ❌',
    'amount': '🎉 Отлично! Пришлите, пожалуйста, сумму, которую необходимо оплатить по указанному QR-коду. 💳',
    'description_pay_request': 'Хотите добавить пояснение к оплате? 💳✨',
    'description_pay_enter': 'Пожалуйста, введите пояснение к оплате. 💬 Это поможет нам лучше Вас понять! 😊',
    'order_process': 'Хотите добавить другие товары в ваш заказ? 🛒✨',
    'complete_order': 'Спасибо за ваш заказ! 🎉 Менеджер внимательно проанализирует вашу заявку и скоро свяжется с '
                      'вами для подтверждения. Хорошего дня! ☀️\n\nЧтобы вернуться в меню, введите /menu.',
    'length_request': 'Пожалуйста, введите длину, ширину и высоту коробки в <b>сантиметрах</b> в формате '
                      'ДлинахШиринахВысота.'
                      '\n\n Пример: 380х285х228',
    'width_request': 'Пожалуйста, введите ширину коробки в сантиметрах. 📏 Пример: 40',
    'height_request': 'Пожалуйста, введите высоту коробки в сантиметрах. 📐 Пример: 40',
    'box_count_request': 'Пожалуйста, введите количество коробок. 📦 Пример: 55',
    'weight_request': 'Пожалуйста, введите массу одной коробки в килограммах. 📦 '
                      '\n\nПример: 7',
    'volume_request': 'Пожалуйста, введите объём одной коробки в <b>кубических метрах</b>. 📦 Пример: 80',
    'density_request': 'Введите, пожалуйста, плотность одной коробки в кг/м3. Пример: 60',
    'delivery_type': 'Чтобы рассчитать стоимость доставки 🚚, нам нужно знать данные о вашем грузе. Пожалуйста, '
                     'выберите один из вариантов:\n\n'
                     '1. Если вам известны длина, ширина, высота каждой коробки 📏📐, вес одной коробки и количество '
                     'коробок 📦, укажите эти параметры.\n\n'
                     '2. Если вам известен общий объём груза 📊 и вес груза, выберите этот вариант (количество '
                     'коробок указывать не нужно).\n\n'
                     'Пожалуйста, выберите, какие параметры вам известны! 😊',
    'delivery_price': '🚚 Стоимость доставки составляет {} долларов для доставки автотранспортом (15-25 дней) 🚗 или {} '
                      'долларов для доставки железнодорожным транспортом (35-45 дней) 🚂💰.\n\nПодтверждаете ли Вы '
                      'доставку? ✅😊',
    'delivery_description_request': 'Хотите добавить пояснение к доставке? 📦✍️',
    'delivery_description_enter': 'Пожалуйста, введите пояснение к доставке. 📝',
    '/start': "Добро пожаловать! 🎉\n\n"
    "Мы рады видеть вас в нашем сервисе, который делает процесс покупки товаров из Китая простым и удобным. 🌏"
    "У нас есть собственные склады в Китае 🇨🇳 и офис в Москве 🇷🇺 — это обеспечивает надёжность и оперативность на "
              "всех этапах работы. ⚙️\n\n"
    "Мы предлагаем вам:\n\n"
    "1. <b>Найти и заказать товар</b> — отправьте фотографию или ссылку на товар, а мы найдём, купим и доставим его "
              "вам.🛍️📸\n"
    "2. <b>Оплатить заказ</b> — если вы уже выбрали товар, но возникли сложности с оплатой, мы решим эту проблему через"
              " проверенные китайские платёжные системы. 💳✅\n"
    "3. <b>Доставить товар в Россию</b> — обеспечим быструю и безопасную доставку прямо до вашего дома. 🚚🏠\n"
    "4. <b>Полный цикл услуг</b> — от поиска до доставки. Всё, что вам нужно — это сделать заказ, а остальное мы "
              "возьмём на себя. 🔄✨\n\n"
    "Мы делаем всё, чтобы покупки из Китая были для вас удобными и надёжными. Спасибо, что выбрали нас! 👌❤️",
    '/menu': '📋 Пожалуйста, выберите нужную услугу из списка',
    '/help': 'По всем вопросам можно обратиться к нашему менеджеру:\n @realname11',
    'other': 'Для продолжения наберите команду /menu',
    'need_dim_format': 'Введите, пожалуйста, размерности в сантиметрах в указанном формате: Длина×Ширина×Высота 📏✖.'
                   '\n\n Пример: 380×285×228'
                   '\n\n Для отмены наберите команду /menu ❌.',

}
PICKUP_ADDRESS: str = load_config().pickup_address


ORDER: dict[str, str] = {
    'status': 'Статус',
    'is_url': 'Есть ли ссылка',
    'url': 'Ссылка',
    'is_photo': 'Есть ли фото',
    'photo': 'Фото',
    'count': 'Количество',
    'is_description': 'Есть ли пояснение',
    'description': 'Пояснение',
    'select_params': 'Выбранные параметры',
    'length': 'Длина коробки',
    'width': 'Ширина коробки',
    'height': 'Высота коробки',
    'volume': 'Объём коробки',
    'density': 'Плотность коробки',
    'car_price': 'Цена доставки автотранспортом',
    'train_price': 'Цена доставки ЖД',
    'bank': 'Банк',
    'amount': 'Сумма к оплате',
    'requisites': 'Реквизиты',
    'delivery_type': 'Тип доставки',
    'weight': 'Вес коробки',
}

LEXICON_COMMANDS: dict[str, str] = {
    '/menu': 'Показать меню магазина',
    '/help': 'Обратиться к менеджеру'
}
