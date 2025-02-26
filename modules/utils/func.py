from aiogram.types import Message
from modules.database.db import get_user_language
from modules.utils.db_utils import get_text_from_db


def is_button_pressed(message: Message, key: str) -> bool:
    """
    Проверяет, совпадает ли текст сообщения с текстом кнопки из БД.
    :param message: Сообщение пользователя.
    :param key: Ключ текста в БД.
    :return: True, если текст совпадает, иначе False.
    """
    user_id = message.chat.id
    user_language = get_user_language(user_id) or 'en'
    button_text = get_text_from_db(user_language, key)
    return message.text == button_text