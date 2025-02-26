import logging
from aiogram import Bot, Dispatcher, F
from modules.main_menu.handlers import register_main_menu_handlers, register_language_handlers
#from modules.language.handlers import register_language_handlers
from modules.profile.handlers import register_profile_handlers
from modules.database.db import init_db
from modules.free_divination.handlers import register_free_divination_handlers
from modules.free_divination.magic_ball import register_magic_ball_handlers
from modules.free_divination.fortune_cookie import register_fortune_cookie_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token="7915755634:AAELbXrvTjkEkCQwY_sb0GDPKiFRPOQGXUQ")  # Замените на ваш реальный токен
dp = Dispatcher()

# Инициализация базы данных
init_db()

# Регистрация обработчиков,
register_main_menu_handlers(dp)
register_language_handlers(dp)
register_profile_handlers(dp)  # Передаём dp в функцию регистрации обработчиков
register_free_divination_handlers(dp)

# Регистрация обработчиков магического шара
register_magic_ball_handlers(dp)

# Регистрация обработчиков печенья с предсказаниями
register_fortune_cookie_handlers(dp)



# Универсальный обработчик для всех остальных сообщений
@dp.message()
async def handle_unexpected_message(message):
    user_id = message.chat.id
    user_text = message.text  # Текст сообщения от пользователя
    # Логируем необработанное сообщение
    print(f"[DEBUG] Необработанное сообщение от пользователя {user_id}: {user_text}")
    # Отправляем пользователю сообщение об ошибке
    error_text = "Неверный формат ввода. Пожалуйста, используйте кнопки меню."
    await message.answer(error_text)

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)