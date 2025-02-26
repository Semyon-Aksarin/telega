from aiogram import F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from modules.database.db import get_user_language, save_user_language, execute_query


# Функция для получения текста из БД
def get_text_from_db(language, key):
    query = "SELECT text FROM translations WHERE key = ? AND language = ?"
    result = execute_query(query, (key, language))
    if result:
        return result[0][0]  # Возвращаем текст из первой строки
    return None

# Функция для регистрации обработчиков главного меню
def register_main_menu_handlers(dp):
    # Обработчик команды /start
    @dp.message(F.text == "/start")
    async def send_welcome(message: Message):
        user_id = message.chat.id
        user_language = get_user_language(user_id) or 'en'  # Получаем язык пользователя
        welcome_text = get_text_from_db(user_language, 'welcome')  # Получаем текст приветствия из БД
        if not welcome_text:
            welcome_text = "Default welcome message"  # Значение по умолчанию, если перевод не найден

        keyboard = ReplyKeyboardBuilder()
        keyboard.add(
            KeyboardButton(text=get_text_from_db(user_language, 'free_divination')),
            KeyboardButton(text=get_text_from_db(user_language, 'premium_divination')),
            KeyboardButton(text=get_text_from_db(user_language, 'profile')),
            KeyboardButton(text=get_text_from_db(user_language, 'change_language'))
        )
        keyboard.adjust(2)
        await message.answer(welcome_text, reply_markup=keyboard.as_markup(resize_keyboard=True))

    # Обработчик кнопки "Бесплатное гадание"
    @dp.message(F.text.in_([
        lambda lang: get_text_from_db(lang, 'free_divination'),  # Динамическое получение текста
        #"Free divination", "Бесплатное гадание"  # Для совместимости со старыми версиями
    ]))
    async def handle_free_divination(message: Message):
        user_id = message.chat.id
        user_language = get_user_language(user_id) or 'en'
        text = get_text_from_db(user_language, 'free_divination')  # Текст подсказки
        if not text:
            text = "Default free divination message"

        keyboard = ReplyKeyboardBuilder()
        keyboard.add(
            KeyboardButton(text=get_text_from_db(user_language, 'magic_ball')),  # Кнопка "Магический шар"
            KeyboardButton(text=get_text_from_db(user_language, 'back_to_menu'))  # Кнопка "Назад в меню"
        )
        keyboard.adjust(2)
        await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))

    # Обработчик кнопки "Платное гадание"
    @dp.message(F.text.in_([
        lambda lang: get_text_from_db(lang, 'premium_divination'),  # Динамическое получение текста
        "Premium divination", "Платное гадание"  # Для совместимости со старыми версиями
    ]))
    async def handle_premium_divination(message: Message):
        user_id = message.chat.id
        user_language = get_user_language(user_id) or 'en'
        text = get_text_from_db(user_language, 'premium_divination')
        if not text:
            text = "Default premium divination message"
        await message.answer(f"Вы выбрали: {text}")

# Функция для регистрации обработчиков языка
def register_language_handlers(dp):
    dp.message.register(change_language, F.text.in_(["Change language (Language)",
                                                     "Сменить язык (Language)",
                                                     "Sprache ändern (Language)",
                                                     "Changer de langue (Language)",
                                                     "Cambia lingua (Language)",
                                                     "Cambiar idioma (Language)",
                                                     "更改语言 (Language)",
                                                     "भाषा बदलें (Language)",
                                                     "언어 변경 (Language)",
                                                     "تغيير اللغة (Language)"]))
    dp.message.register(select_language, F.text.in_([
        "🇬🇧 English", "🇷🇺 Русский", "🇩🇪 Deutsch", "🇫🇷 Français",
        "🇮🇹 Italiano", "🇪🇸 Español", "🇨🇳 中文", "🇮🇳 हिन्दी",
        "🇰🇷 한국어", "🇸🇦 العربية"
    ]))

# Обработчик кнопки "Сменить язык"
async def change_language(message: Message):
    user_id = message.chat.id
    user_language = get_user_language(user_id) or "ru"  # По умолчанию язык 'ru'

    # Создаём клавиатуру с кнопками выбора языка (с флагами)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇬🇧 English"),  # Английский
                KeyboardButton(text="🇷🇺 Русский"),  # Русский
                KeyboardButton(text="🇩🇪 Deutsch"),  # Немецкий
                KeyboardButton(text="🇫🇷 Français")  # Французский
            ],
            [
                KeyboardButton(text="🇮🇹 Italiano"),  # Итальянский
                KeyboardButton(text="🇪🇸 Español"),  # Испанский
                KeyboardButton(text="🇨🇳 中文"),     # Китайский
                KeyboardButton(text="🇮🇳 हिन्दी")   # Хинди
            ],
            [
                KeyboardButton(text="🇰🇷 한국어"),  # Корейский
                KeyboardButton(text="🇸🇦 العربية"), # Арабский
                KeyboardButton(text=get_text_from_db(user_language, "back_to_menu"))  # Кнопка "Назад в меню"
            ]
        ],
        resize_keyboard=True
    )

    # Отправляем сообщение с выбором языка
    text = get_text_from_db(user_language, "select_language")
    if not text:
        text = "Default select language message"
    await message.answer(text, reply_markup=keyboard)

# Обработчик выбора языка
async def select_language(message: Message):
    print("[DEBUG] Обработчик select_language вызван")
    user_id = message.chat.id
    selected_language = None

    if message.text in ["🇬🇧 English", "English"]:
        selected_language = "en"
    elif message.text in ["🇷🇺 Русский", "Русский"]:
        selected_language = "ru"
    elif message.text in ["🇩🇪 Deutsch", "Deutsch"]:
        selected_language = "de"
    elif message.text in ["🇫🇷 Français", "Français"]:
        selected_language = "fr"
    elif message.text in ["🇮🇹 Italiano", "Italiano"]:
        selected_language = "it"
    elif message.text in ["🇪🇸 Español", "Español"]:
        selected_language = "es"
    elif message.text in ["🇨🇳 中文", "中文"]:
        selected_language = "zh"
    elif message.text in ["🇮🇳 हिन्दी", "हिन्दी"]:
        selected_language = "hi"
    elif message.text in ["🇰🇷 한국어", "한국어"]:
        selected_language = "ko"
    elif message.text in ["🇸🇦 العربية", "العربية"]:
        selected_language = "ar"

    if selected_language:
        # Сохраняем выбранный язык в базу данных
        save_user_language(user_id, selected_language)

        # Отправляем подтверждение об изменении языка
        confirmation_text = get_text_from_db(selected_language, f"language_changed_to_{selected_language}")
        if not confirmation_text:
            confirmation_text = "Language changed successfully!"
        await message.answer(confirmation_text)

        # Возвращаемся в главное меню
        main_menu_text = get_text_from_db(selected_language, "welcome")
        if not main_menu_text:
            main_menu_text = "Default welcome message"

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=get_text_from_db(selected_language, "free_divination")),
                    KeyboardButton(text=get_text_from_db(selected_language, "premium_divination"))
                ],
                [
                    KeyboardButton(text=get_text_from_db(selected_language, "profile")),
                    KeyboardButton(text=get_text_from_db(selected_language, "change_language"))
                ]
            ],
            resize_keyboard=True
        )
        await message.answer(main_menu_text, reply_markup=keyboard)
    else:
        # Если выбран некорректный язык, отправляем ошибку
        user_language = get_user_language(user_id) or "ru"
        error_text = get_text_from_db(user_language, "invalid_input")
        if not error_text:
            error_text = "Invalid input"
        await message.answer(error_text)