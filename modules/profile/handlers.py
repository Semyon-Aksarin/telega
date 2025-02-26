from aiogram import F
import json
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from modules.profile.texts import get_text
from modules.database.db import get_user_data, save_user_data, get_user_language, execute_query
from modules.profile.utils import get_zodiac_sign, get_chinese_zodiac_animal, get_color_by_birthdate, get_tree_by_birthdate, get_stone_by_birthdate, get_element_by_zodiac, get_planet_by_zodiac, get_life_path_number, get_totem_animal
from modules.main_menu.handlers import get_text_from_db

# Определение состояний
class EditProfileStates(StatesGroup):
    AWAITING_BIRTH_YEAR = State()
    AWAITING_BIRTH_MONTH = State()
    AWAITING_BIRTH_DAY = State()
    AWAITING_BIRTH_HOUR = State()
    AWAITING_BIRTH_MINUTE = State()
    AWAITING_BIRTHPLACE = State()

# Функция для регистрации обработчиков
def register_profile_handlers(dp):
    print("[DEBUG] Регистрация обработчиков профиля...")

    # Обработчик кнопки "Профиль"
    async def handle_profile(message: Message):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        text = get_text(user_language, 'profile_edit_prompt')
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(
            KeyboardButton(text=get_text(user_language, 'edit_profile')),  # Кнопка "Редактировать профиль"
            KeyboardButton(text=get_text(user_language, 'view_profile')),  # Кнопка "Просмотреть профиль"
            KeyboardButton(text=get_text(user_language, 'detailed_profile')),  # Кнопка "Подробный профиль"
            KeyboardButton(text=get_text(user_language, 'back_to_menu'))   # Кнопка "Назад в меню"
        )
        keyboard.adjust(2)
        await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))

    dp.message.register(handle_profile, F.text.in_(["Profile", "Профиль"]))

    # Обработчик кнопки "Редактировать профиль"
    async def start_edit_profile(message: Message, state: FSMContext):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        text = get_text(user_language, 'edit_profile_enter_birth_year')
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(
            KeyboardButton(text=get_text(user_language, 'back_to_menu'))  # Кнопка "Назад в меню"
        )
        keyboard.adjust(2)
        await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(EditProfileStates.AWAITING_BIRTH_YEAR)

    dp.message.register(start_edit_profile, F.text.in_(["Edit Profile", "Редактировать профиль"]))

    # Обработчик кнопки "Назад в меню"
    async def back_to_menu(message: Message, state: FSMContext):
        user_id = message.chat.id
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        # Очищаем состояние
        await state.clear()

        # Возвращаемся в главное меню
        text = get_text_from_db(user_language, 'welcome')  # Текст берется из БД
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(
            KeyboardButton(text=get_text_from_db(user_language, 'free_divination')),  # Бесплатное гадание
            KeyboardButton(text=get_text_from_db(user_language, 'premium_divination')),  # Платное гадание
            KeyboardButton(text=get_text_from_db(user_language, 'profile')),  # Профиль
            KeyboardButton(text=get_text_from_db(user_language, 'change_language'))  # Сменить язык
        )
        keyboard.adjust(2)
        await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))

    # Обработчик состояния AWAITING_BIRTH_YEAR
    async def process_birth_year(message: Message, state: FSMContext):
        # Проверяем, была ли нажата кнопка "Назад в меню"
        if message.text in ["Back to menu", "Назад в меню"]:
            await back_to_menu(message, state)
            return

        user_id = message.chat.id
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        try:
            birth_year = int(message.text.strip())
            if birth_year < 1900 or birth_year > 2100:
                raise ValueError("Year must be between 1900 and 2100.")

            await state.update_data(birth_year=birth_year)
            text = get_text(user_language, 'edit_profile_enter_birth_month')
            await message.answer(text)
            await state.set_state(EditProfileStates.AWAITING_BIRTH_MONTH)

        except ValueError as ve:
            error_text = get_text(user_language, 'invalid_input') + f"\nError: {ve}"
            await message.answer(error_text)

    dp.message.register(process_birth_year, EditProfileStates.AWAITING_BIRTH_YEAR)



    # Обработчик состояния AWAITING_BIRTH_MONTH
    async def process_birth_month(message: Message, state: FSMContext):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        try:
            birth_month = int(message.text.strip())
            if birth_month < 1 or birth_month > 12:
                raise ValueError("Month must be between 1 and 12.")

            await state.update_data(birth_month=birth_month)
            text = get_text(user_language, 'edit_profile_enter_birth_day')
            await message.answer(text)
            await state.set_state(EditProfileStates.AWAITING_BIRTH_DAY)

        except ValueError as ve:
            error_text = get_text(user_language, 'invalid_input') + f"\nError: {ve}"
            await message.answer(error_text)

    dp.message.register(process_birth_month, EditProfileStates.AWAITING_BIRTH_MONTH)

    # Обработчик состояния AWAITING_BIRTH_DAY
    async def process_birth_day(message: Message, state: FSMContext):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        try:
            birth_day = int(message.text.strip())
            if birth_day < 1 or birth_day > 31:
                raise ValueError("Day must be between 1 and 31.")

            await state.update_data(birth_day=birth_day)
            text = get_text(user_language, 'edit_profile_enter_birth_hour')
            await message.answer(text)
            await state.set_state(EditProfileStates.AWAITING_BIRTH_HOUR)

        except ValueError as ve:
            error_text = get_text(user_language, 'invalid_input') + f"\nError: {ve}"
            await message.answer(error_text)

    dp.message.register(process_birth_day, EditProfileStates.AWAITING_BIRTH_DAY)

    # Обработчик состояния AWAITING_BIRTH_HOUR
    async def process_birth_hour(message: Message, state: FSMContext):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        try:
            birth_hour = int(message.text.strip())
            if birth_hour < 0 or birth_hour > 23:
                raise ValueError("Hour must be between 0 and 23.")

            await state.update_data(birth_hour=birth_hour)
            text = get_text(user_language, 'edit_profile_enter_birth_minute')
            await message.answer(text)
            await state.set_state(EditProfileStates.AWAITING_BIRTH_MINUTE)

        except ValueError as ve:
            error_text = get_text(user_language, 'invalid_input') + f"\nError: {ve}"
            await message.answer(error_text)

    dp.message.register(process_birth_hour, EditProfileStates.AWAITING_BIRTH_HOUR)

    # Обработчик состояния AWAITING_BIRTH_MINUTE
    async def process_birth_minute(message: Message, state: FSMContext):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        try:
            birth_minute = int(message.text.strip())
            if birth_minute < 0 or birth_minute > 59:
                raise ValueError("Minute must be between 0 and 59.")

            await state.update_data(birth_minute=birth_minute)
            text = get_text(user_language, 'edit_profile_enter_birthplace')
            await message.answer(text)
            await state.set_state(EditProfileStates.AWAITING_BIRTHPLACE)

        except ValueError as ve:
            error_text = get_text(user_language, 'invalid_input') + f"\nError: {ve}"
            await message.answer(error_text)

    dp.message.register(process_birth_minute, EditProfileStates.AWAITING_BIRTH_MINUTE)

    # Обработчик состояния AWAITING_BIRTHPLACE
    async def process_birthplace(message: Message, state: FSMContext):
        user_id = message.chat.id

        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

        birthplace = message.text.strip()
        data = await state.get_data()
        data['birthplace'] = birthplace

        # Определяем знак зодиака
        zodiac_sign = get_zodiac_sign(data['birth_day'], data['birth_month'])

        # Определяем животное по китайскому календарю
        chinese_zodiac_animal = get_chinese_zodiac_animal(data['birth_year'])

        # Определяем дерево на основе даты рождения
        birth_date = f"{data['birth_day']:02d}.{data['birth_month']:02d}"
        tree_data = get_tree_by_birthdate(birth_date)
        tree = tree_data["name"] if tree_data else "Неизвестное дерево"

        # Определяем дерево, камень, цвет, стихию, планету, число судьбы и тотемное животное
        stone = get_stone_by_birthdate(data['birth_day'], data['birth_month'])
        color = get_color_by_birthdate(data['birth_month'])
        element = get_element_by_zodiac(zodiac_sign)
        planet = get_planet_by_zodiac(zodiac_sign)
        life_path_number = get_life_path_number(data['birth_year'], data['birth_month'], data['birth_day'])
        totem_animal = get_totem_animal(data['birth_month'])

        # Добавляем все данные
        data['zodiac_sign'] = zodiac_sign
        data['chinese_zodiac_animal'] = chinese_zodiac_animal
        data['tree'] = tree
        data['stone'] = stone
        data['color'] = color
        data['element'] = element  # Добавляем стихию
        data['planet'] = planet  # Добавляем планету
        data['life_path_number'] = life_path_number  # Добавляем число судьбы
        data['totem_animal'] = totem_animal  # Добавляем тотемное животное

        # Сохраняем данные в базу
        save_user_data(user_id, data)  # Вызываем функцию сохранения данных
        print(f"[DEBUG] Сохранены данные пользователя {user_id}: {data}")

        # Очищаем состояние
        await state.clear()

        # Показываем обновлённый профиль
        await view_profile(message)

        text = get_text(user_language, 'edit_profile_success')
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(KeyboardButton(text=get_text(user_language, 'back_to_menu')))
        await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))

    dp.message.register(process_birthplace, EditProfileStates.AWAITING_BIRTHPLACE)

    def load_translations(language_code, category, category_key):
        try:
            file_path = f"modules/static/{category}.json"
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Проверяем, существует ли ключ category_key
            if category_key not in data:
                print(f"[ERROR] Key '{category_key}' not found in {file_path}.")
                return {}

            translations = {}
            category_data = data[category_key]

            # Если данные - список
            if isinstance(category_data, list):
                for item in category_data:
                    # Убедитесь, что item — это словарь с ожидаемой структурой
                    if not isinstance(item, dict) or "name" not in item or not isinstance(item["name"], dict):
                        print(f"[ERROR] Invalid item structure: {item}")
                        continue
                    # Извлекаем оригинальное имя (например, русское) как ключ
                    original_name = item["name"].get("ru")
                    if original_name:
                        translations[original_name] = item["name"]

            # Если данные - словарь
            elif isinstance(category_data, dict):
                for key, item in category_data.items():
                    # Убедитесь, что item — это словарь с переводами
                    if not isinstance(item, dict):
                        print(f"[ERROR] Invalid item structure: {item}")
                        continue
                    # Используем оригинальное имя (например, русское) как ключ
                    original_name = item.get("ru")
                    if original_name:
                        translations[original_name] = item

            else:
                print(f"[ERROR] Invalid data type for key '{category_key}'. Expected list or dict.")
                return {}

            return translations

        except FileNotFoundError:
            print(f"[ERROR] JSON file for category '{category}' and language '{language_code}' not found.")
            return {}

    def translate_value(category, value, language_code):
        """
        Переводит значение на язык пользователя.
        :param category: Категория перевода (например, 'trees', 'stones', 'colors').
        :param value: Значение для перевода (например, 'Apple', 'Diamond').
        :param language_code: Код языка пользователя.
        :return: Переведенное значение или оригинальное, если перевод не найден.
        """
        translations = load_translations(language_code, category, category)
        if value in translations:
            return translations[value].get(language_code, value)  # Возвращаем перевод или оригинал
        return value

    # Обработчик кнопки "Просмотреть профиль"
    @dp.message(F.text.in_([
        "View Profile", "Просмотреть профиль"
    ]))
    async def view_profile(message: Message):
        user_id = message.chat.id
        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        if not user_data:
            user_language = get_user_language(user_id)  # По умолчанию язык 'ru'
            text = get_text(user_language, 'profile_not_found')
            await message.answer(text)
            return

        # Разбираем данные пользователя
        (
            _, user_language, birth_year, birth_month, birth_day,
            birth_hour, birth_minute, birthplace, zodiac_sign,
            chinese_zodiac_animal, tree, stone, color,
            element, planet, life_path_number, totem_animal
        ) = user_data

        # Переводим значения на язык пользователя
        zodiac_sign = translate_value("zodiac_signs", zodiac_sign, user_language)
        chinese_zodiac_animal = translate_value("chinese_zodiac_animal", chinese_zodiac_animal, user_language)
        stone = translate_value("stone", stone, user_language)
        color = translate_value("color", color, user_language)
        element = translate_value("element", element, user_language)
        planet = translate_value("planet", planet, user_language)
        totem_animal = translate_value("totem_animal", totem_animal, user_language)
        tree = translate_value("tree", tree, user_language)


        # Формируем текст профиля
        profile_text = get_text(user_language, 'profile_view').format(
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            birth_hour=birth_hour,
            birth_minute=birth_minute,
            birthplace=birthplace,
            zodiac_sign=zodiac_sign,
            chinese_zodiac_animal=chinese_zodiac_animal,
            tree=tree,
            stone=stone,
            color=color,
            element=element,  # Добавляем стихию
            planet=planet,  # Добавляем планету
            life_path_number=life_path_number,  # Добавляем число судьбы
            totem_animal=totem_animal  # Добавляем тотемное животное
        )

        # Создаём клавиатуру с кнопкой "Назад в меню"
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(KeyboardButton(text=get_text(user_language, 'back_to_menu')))
        await message.answer(profile_text, reply_markup=keyboard.as_markup(resize_keyboard=True))


# Обработчик кнопки "Подробный профиль"
    @dp.message(F.text.in_([
        "Detailed profile", "Подробный профиль"
    ]))
    async def view_profile(message: Message):
        user_id = message.chat.id
        # Получаем данные пользователя из базы
        user_data = get_user_data(user_id)
        if not user_data:
            user_language = get_user_language(user_id)  # По умолчанию язык 'ru'
            text = get_text(user_language, 'profile_not_found')
            await message.answer(text)
            return

        # Разбираем данные пользователя
        (
            _, user_language, birth_year, birth_month, birth_day,
            birth_hour, birth_minute, birthplace, zodiac_sign,
            chinese_zodiac_animal, tree, stone, color,
            element, planet, life_path_number, totem_animal
        ) = user_data

        # Формируем текст профиля
        profile_text = get_text(user_language, 'profile_view').format(
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            birth_hour=birth_hour,
            birth_minute=birth_minute,
            birthplace=birthplace,
            zodiac_sign=zodiac_sign,
            chinese_zodiac_animal=chinese_zodiac_animal,
            tree=tree,
            stone=stone,
            color=color,
            element=element,  # Добавляем стихию
            planet=planet,  # Добавляем планету
            life_path_number=life_path_number,  # Добавляем число судьбы
            totem_animal=totem_animal  # Добавляем тотемное животное
        )

        # Создаём клавиатуру с кнопкой "Назад в меню"
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(KeyboardButton(text=get_text(user_language, 'back_to_menu')))
        await message.answer(profile_text, reply_markup=keyboard.as_markup(resize_keyboard=True))

# Обработчик кнопки "Назад в меню"
async def back_to_menu(message: Message, state: FSMContext):
    user_id = message.chat.id

    # Получаем данные пользователя из базы
    user_data = get_user_data(user_id)
    user_language = user_data[1] if user_data else 'ru'  # По умолчанию язык 'ru'

    # Очищаем состояние
    await state.clear()

