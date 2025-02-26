from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from modules.free_divination.texts import get_text
from modules.database.db import get_user_language
from modules.main_menu.handlers import get_text_from_db
import os

dp = Dispatcher()\

# Список ответов магического шара для разных языков
MAGIC_BALL_ANSWERS = {
    'en': [
        "It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
        "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
        "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
        "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
        "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good",
        "Very doubtful"
    ],
    'ru': [
        "Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да", "Можешь быть уверен в этом",
        "Мне кажется — да", "Вероятнее всего", "Хорошие перспективы", "Знаки говорят — да", "Да",
        "Пока не ясно, попробуй снова", "Спроси позже", "Лучше не рассказывать", "Сейчас нельзя предсказать",
        "Сконцентрируйся и спроси опять", "Даже не думай", "Мой ответ — нет", "По моим данным — нет",
        "Перспективы не очень хорошие", "Весьма сомнительно"
    ]
}

def get_magic_ball_answer(language='en'):
    """
    Возвращает случайный ответ магического шара на указанном языке.
    :param language: Язык ('en', 'ru').
    :return: Текст ответа на указанном языке.
    """
    import random
    return random.choice(MAGIC_BALL_ANSWERS.get(language, MAGIC_BALL_ANSWERS['en']))

@dp.message(F.text.in_(["Magic Ball", "Магический шар"]))
async def magic_ball_instruction(message: Message):
    print(f"[DEBUG] Получено сообщение: {message.text}")
    user_language = get_user_language(message.chat.id)
    instruction_text = get_text(user_language, 'magic_ball_instruction')
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=get_text(user_language, 'give_answer')),
        KeyboardButton(text=get_text_from_db(user_language, 'back_to_menu'))
    )
    keyboard.adjust(2)
    await message.answer(instruction_text, reply_markup=keyboard.as_markup(resize_keyboard=True))


async def give_answer(message: Message):
    user_language = get_user_language(message.chat.id)

    # Путь к GIF-файлу
    gif_path = "static/images/magic_ball.gif"

    # Проверяем существование файла
    if not os.path.exists(gif_path):
        error_text = "Извините, анимация временно недоступна."
        await message.answer(error_text)
        return

    # Получаем случайный ответ магического шара
    answer = get_magic_ball_answer(user_language)

    # Отправляем анимацию с ответом
    await message.answer_animation(animation=FSInputFile(gif_path), caption=answer)

def register_magic_ball_handlers(dp):
    dp.message.register(magic_ball_instruction, F.text.in_([
        "Magic Ball", "Магический шар"
    ]))
    dp.message.register(give_answer, F.text.in_([
        "Give Answer", "Дать ответ"
    ]))
    dp.message.register(return_to_main_menu, F.text.in_([
        "Back to menu", "Назад в меню"
    ]))


async def return_to_main_menu(message: Message):
    """
    Возвращение в главное меню.
    """
    user_language = get_user_language(message.chat.id)  # Получаем язык пользователя
    text = get_text(user_language, 'welcome')  # Текст приветствия
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=get_text(user_language, 'free_divination')),  # Бесплатное гадание
        KeyboardButton(text=get_text(user_language, 'premium_divination')),  # Платное гадание
        KeyboardButton(text=get_text(user_language, 'profile')),  # Профиль
        KeyboardButton(text=get_text(user_language, 'change_language'))  # Сменить язык
    )
    keyboard.adjust(2)
    await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))