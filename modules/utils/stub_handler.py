from aiogram.types import Message
from modules.profile.texts import get_text  # Импортируем функцию для получения текстов
from modules.database.db import get_user_data


async def send_stub_message(message: Message, text_key: str):
    user_id = message.chat.id
    user_data_tuple = get_user_data(user_id)  # Получаем кортеж
    user_data = {
        "user_id": user_data_tuple[0],
        "language": user_data_tuple[1],
        "birth_year": user_data_tuple[2],
        "birth_month": user_data_tuple[3],
        "birth_day": user_data_tuple[4],
        "birth_hour": user_data_tuple[5],
        "birth_minute": user_data_tuple[6],
        "birthplace": user_data_tuple[7],
        "zodiac_sign": user_data_tuple[8],
        "chinese_zodiac_animal": user_data_tuple[9]
    }
    user_language = user_data.get("language", "ru")  # По умолчанию язык 'ru'

    # Получаем текст заглушки
    text = get_text(user_language, text_key)

    # Отправляем сообщение
    await message.answer(text)