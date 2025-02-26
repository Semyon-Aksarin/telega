def get_text(language, key):
    texts = {
        "welcome": {
            "ru": "Добро пожаловать! Для начала использования бота создайте профиль и выберите язык.",
            "en": "Welcome! To start using the bot, please create a profile."
        },
        "free_divination": {
            "ru": "Бесплатное гадание",
            "en": "Free divination"
        },
        "premium_divination": {
            "ru": "Платное гадание",
            "en": "Premium divination"
        },
        "profile": {
            "ru": "Профиль",
            "en": "Profile"
        },
        "select_language": {
            "ru": "Выберите ваш язык:",
            "en": "Select your language:"
        },
        "magic_ball": {
            "en": "Magic Ball",
            "ru": "Магический шар"
        },
        "language_changed_to_en": {
            "ru": "Язык изменён на английский.",
            "en": "Language changed to English."
        },
        "language_changed_to_ru": {
            "ru": "Язык изменён на русский.",
            "en": "Language changed to Russian."
        },
        "back_to_menu": {
            "ru": "Назад в меню",
            "en": "Back to menu"
        },
        "change_language": {
            "ru": "Сменить язык",
            "en": "Change language"
        }
    }
    return texts[key][language]