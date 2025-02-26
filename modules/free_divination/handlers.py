from aiogram import F, Dispatcher
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from modules.free_divination.texts import get_text
from modules.database.db import get_user_language  # Импортируем функцию получения языка
from modules.utils.stub_handler import send_stub_message
from .random_advice import random_advice
from .wheel_of_fate import wheel_of_fate
from .one_card_tarot import one_card_tarot
from modules.main_menu.handlers import get_text_from_db

dp = Dispatcher()

# Регистрация обработчиков бесплатных гаданий
def register_free_divination_handlers(dp):
    dp.message.register(handle_free_divination, F.text.in_([
        "Free divination", "Бесплатное гадание"
    ]))
    dp.message.register(horoscope_stub, F.text.in_(["Horoscope", "Гороскоп"]))
    dp.message.register(one_card_tarot, F.text.in_(["One Card Tarot", "Таро по 1 карте"]))
    dp.message.register(random_advice, F.text.in_(["Random Advice", "Случайный совет"]))
    dp.message.register(wheel_of_fate, F.text.in_(["Wheel of Fate", "Колесо судьбы"]))
    dp.message.register(one_card_tarot, F.text.in_(["One Card Tarot", "Гадание на одной карте"]))
    # Добавьте сюда регистрацию других обработчиков (например, магический шар)

# Обработчик кнопки "Бесплатное гадание"
async def handle_free_divination(message: Message):
    user_language = get_user_language(message.chat.id)  # Получаем язык пользователя
    text = get_text(user_language, 'free_divination_prompt')  # Текст подсказки
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=get_text_from_db(user_language, 'magic_ball')),  # Кнопка "Магический шар"
        KeyboardButton(text=get_text_from_db(user_language, 'fortune_cookie')),
        KeyboardButton(text=get_text_from_db(user_language, 'horoscope')),  # Гороскоп
        KeyboardButton(text=get_text_from_db(user_language, 'one_card_tarot')),  # Таро по 1 карте
        KeyboardButton(text=get_text_from_db(user_language, 'random_advice')),  # Кнопка "Назад в меню"
        KeyboardButton(text=get_text_from_db(user_language, 'wheel_of_fate')),  # Кнопка "Назад в меню"
        KeyboardButton(text=get_text_from_db(user_language, 'back_to_menu'))  # Кнопка "Назад в меню"
    )
    keyboard.adjust(2)
    await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(["Horoscope", "Гороскоп"]))
async def horoscope_stub(message: Message):
    await send_stub_message(message, "horoscope_unavailable")

