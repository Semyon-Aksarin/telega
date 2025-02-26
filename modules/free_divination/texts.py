def get_text(language, key):
    texts = {
        "magic_ball_instruction": {
            "en": "Welcome to the Magic Ball! Ask your question and press 'Give Answer'.",
            "ru": "Добро пожаловать в Магический Шар! Задайте свой вопрос и нажмите 'Дать ответ'."
        },
        "give_answer": {
            "en": "Give Answer",
            "ru": "Дать ответ"
        },
        "back_to_menu": {
            "en": "Back to menu",
            "ru": "Назад в меню"
        },
        'free_divination': {
            'ru': 'Бесплатное гадание',
            'en': 'Free divination',
            # Добавьте другие языки, если они поддерживаются
        },
        "premium_divination": {
            "ru": "Платное гадание",
            "en": "Premium divination"
        },
        "change_language": {
            "ru": "Сменить язык",
            "en": "Change language"
        },
        "profile": {
            "ru": "Профиль",
            "en": "Profile"
        },
        "welcome": {
            "en": "Welcome to the main menu!",
            "ru": "Добро пожаловать в главное меню!"

        },
        "free_divination_prompt": {
            "en": "You have chosen free divination. Select an option:",
            "ru": "Вы выбрали бесплатное гадание. Выберите опцию:"
        },
        "magic_ball": {
            "en": "Magic Ball",
            "ru": "Магический шар"
        },
        "fortune_cookie_instruction": {
            "en": "Welcome to Fortune Cookie! Press 'Get Fortune' to receive your prediction.",
            "ru": "Добро пожаловать в гадание Печенье! Нажмите 'Получить предсказание', чтобы получить ваше предсказание."
        },
        "get_fortune": {
            "en": "Get Fortune",
            "ru": "Получить предсказание"
        },
        "horoscope": {
            "en": "Horoscope",
            "ru": "Гороскоп"
        },
        "horoscope_unavailable": {
            "en": "The horoscope feature is currently unavailable. Stay tuned for updates!",
            "ru": "Функция гороскопа временно недоступна. Следите за обновлениями!"
        },
        "feature_unavailable": {
            "en": "This feature is currently unavailable. Stay tuned for updates!",
            "ru": "Эта функция временно недоступна. Следите за обновлениями!"
        },
        "one_card_tarot": {
            "en": "One Card Tarot",
            "ru": "Таро по 1 карте"
        },
        "one_card_tarot_unavailable": {
            "en": "The One Card Tarot feature is currently unavailable. Stay tuned for updates!",
            "ru": "Функция 'Таро по 1 карте' временно недоступна. Следите за обновлениями!"
        },
        "wheel_of_fate": {
            "en": "Wheel of Fate",
            "ru": "Колесо судьбы"
        },
        "random_advice": {
            "en": "Random Advice",
            "ru": "Случайный совет"
        },
        "en": {
            "one_card_tarot": "One Card Tarot",
            "back_to_menu": "Back to menu",
        },
        "ru": {
            "one_card_tarot": "Гадание на одной карте",
            "back_to_menu": "Назад в меню",
        },
        "fortune_cookie": {
            "en": "Fortune Cookie",
            "ru": "Печенье с предсказанием"
        }
    }
    return texts[key][language]