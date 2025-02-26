from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from modules.free_divination.texts import get_text
from modules.database.db import get_user_language

dp = Dispatcher()


# Список предсказаний для разных языков
FORTUNE_COOKIES = {
    'en': [
        "An unexpected opportunity will bring you great joy.",
        "You will find success in your current endeavors.",
        "A pleasant surprise awaits you soon.",
        "Your hard work will pay off in the near future.",
        "Good news is coming your way.",
        "You will meet someone who will change your life.",
        "Today is a good day to start something new.",
        "Trust your instincts; they will guide you well.",
        "A small act of kindness will bring you happiness.",
        "You are destined for greatness."
    ],
    'ru': [
        "Неожиданная возможность принесет вам большую радость.",
        "Вы найдете успех в текущих начинаниях.",
        "Вас ждет приятный сюрприз в ближайшее время.",
        "Ваш труд скоро принесет свои плоды.",
        "Хорошие новости идут к вам.",
        "Вы встретите человека, который изменит вашу жизнь.",
        "Сегодня отличный день, чтобы начать что-то новое.",
        "Доверяйте своей интуиции — она вас не подведет.",
        "Маленький добрый поступок принесет вам счастье.",
        "Вы предназначены для великих дел."
    ]
}

def get_fortune_cookie(language='en'):
    """
    Возвращает случайное предсказание на указанном языке.
    :param language: Язык ('en', 'ru').
    :return: Текст предсказания на указанном языке.
    """
    import random
    return random.choice(FORTUNE_COOKIES.get(language, FORTUNE_COOKIES['en']))

@dp.message(F.text.in_(["Fortune Cookie", "Печенье с предсказанием"]))
async def fortune_cookie_instruction(message: Message):
    user_language = get_user_language(message.chat.id)
    instruction_text = get_text(user_language, 'fortune_cookie_instruction')
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=get_text(user_language, 'get_fortune')),
        KeyboardButton(text=get_text(user_language, 'back_to_menu'))
    )
    keyboard.adjust(2)
    await message.answer(instruction_text, reply_markup=keyboard.as_markup(resize_keyboard=True))

async def get_fortune(message: Message):
    user_language = get_user_language(message.chat.id)
    fortune = get_fortune_cookie(user_language)
    await message.answer(fortune)

def register_fortune_cookie_handlers(dp):
    dp.message.register(fortune_cookie_instruction, F.text.in_([
        "Fortune Cookie", "Печенье с предсказанием"
    ]))
    dp.message.register(get_fortune, F.text.in_([
        "Get Fortune", "Получить предсказание"
    ]))