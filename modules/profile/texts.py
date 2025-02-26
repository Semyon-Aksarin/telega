def get_text(language, key):
    texts = {
        "profile_edit_prompt": {
            "ru": "Нажмите 'Редактировать профиль', чтобы начать.",
            "en": "Click 'Edit Profile' to begin."
        },
        "edit_profile_enter_birth_year": {
            "ru": "Введите год рождения:",
            "en": "Enter your birth year:"
        },
        "edit_profile_enter_birth_month": {
            "ru": "Введите месяц рождения (1-12):",
            "en": "Enter your birth month (1-12):"
        },
        "edit_profile_enter_birth_day": {
            "ru": "Введите день рождения (1-31):",
            "en": "Enter your birth day (1-31):"
        },
        "edit_profile_enter_birth_hour": {
            "ru": "Введите час рождения (0-23):",
            "en": "Enter your birth hour (0-23):"
        },
        "edit_profile_enter_birth_minute": {
            "ru": "Введите минуту рождения (0-59):",
            "en": "Enter your birth minute (0-59):"
        },
        "edit_profile_enter_birthplace": {
            "ru": "Введите место рождения:",
            "en": "Enter your birthplace:"
        },
        "edit_profile_success": {
            "ru": "Профиль успешно обновлен!",
            "en": "Profile updated successfully!"
        },
        "invalid_input": {
            "ru": "Неверный формат ввода.",
            "en": "Invalid input format."
        },
        "edit_profile": {
            "ru": "Редактировать профиль",
            "en": "Edit Profile"
        },
        "view_profile": {
            "ru": "Просмотреть профиль",
            "en": "View Profile"
        },
        "detailed_profile": {
            "ru": "Подробный профиль",
            "en": "Detailed profile"
        },
        "profile_not_found": {
            "ru": "Профиль не найден. Пожалуйста, создайте профиль.",
            "en": "Profile not found. Please create a profile."
        },
        "profile_view": {
            "ru": (
                "Ваш профиль:\n"
                "Дата рождения: {birth_year}-{birth_month:02d}-{birth_day:02d} {birth_hour:02d}:{birth_minute:02d}\n"
                "Место рождения: {birthplace}\n"
                "Знак зодиака: {zodiac_sign}\n"
                "Китайское животное: {chinese_zodiac_animal}\n"
                "Дерево: {tree}\n"
                "Камень: {stone}\n"
                "Цвет: {color}\n"
                "Стихия: {element}\n"
                "Планета-покровитель: {planet}\n"
                "Число судьбы: {life_path_number}\n"
                "Тотемное животное: {totem_animal}"
            ),
            "en": (
                "Your profile:\n"
                "Date of birth: {birth_year}-{birth_month:02d}-{birth_day:02d} {birth_hour:02d}:{birth_minute:02d}\n"
                "Place of birth: {birthplace}\n"
                "Zodiac sign: {zodiac_sign}\n"
                "Chinese animal: {chinese_zodiac_animal}\n"
                "Tree: {tree}\n"
                "Stone: {stone}\n"
                "Color: {color}\n"
                "Element: {element}\n"
                "Ruling planet: {planet}\n"
                "Life path number: {life_path_number}\n"
                "Totem animal: {totem_animal}"
            )
        },
        "back_to_menu": {
            "ru": "Назад в меню",
            "en": "Back to menu"
        },
        "welcome": {
            "ru": "Добро пожаловать!",
            "en": "Welcome!"
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
        "horoscope": {
            "en": "Horoscope",
            "ru": "Гороскоп"
        },
        "horoscope_unavailable": {
            "en": "The horoscope feature is currently unavailable. Stay tuned for updates!",
            "ru": "Функция гороскопа временно недоступна. Следите за обновлениями!"
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
        "change_language": {
            "ru": "Сменить язык",
            "en": "Change language"
        }
    }
    return texts[key][language]