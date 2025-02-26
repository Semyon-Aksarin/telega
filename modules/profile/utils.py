import json
from pathlib import Path


def load_druid_trees():
    """
    Загружает данные о деревьях друидов из JSON-файла.
    :return: Список словарей с информацией о деревьях.
    """
    # Определяем путь к файлу
    file_path = Path(__file__).parent.parent / "static" / "druid_trees.json"
    print(f"[DEBUG] Путь к JSON-файлу: {file_path}")  # Отладочный вывод

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)["trees"]


def get_tree_by_birthdate(birth_date):
    """
    Определяет дерево по дате рождения на основе кельтского гороскопа.
    :param birth_date: Дата рождения в формате 'DD.MM'.
    :return: Словарь с информацией о дереве или None, если дерево не найдено.
    """
    # Преобразуем дату рождения в числа
    try:
        birth_day, birth_month = map(int, birth_date.split("."))
    except ValueError:
        print("[ERROR] Неверный формат даты рождения.")
        return None

    trees = load_druid_trees()
    for tree in trees:
        start_date = tree["dates"][0]
        end_date = tree["dates"][1]
        start_day, start_month = map(int, start_date.split("."))
        end_day, end_month = map(int, end_date.split("."))

        # Проверяем, попадает ли дата рождения в диапазон
        if start_month < end_month:
            if (birth_month == start_month and birth_day >= start_day) or \
               (birth_month == end_month and birth_day <= end_day) or \
               (start_month < birth_month < end_month):
                return tree
        else:
            # Если диапазон пересекает год (например, 22.12 - 10.01)
            if (birth_month >= start_month or birth_month <= end_month) and \
               ((birth_month == start_month and birth_day >= start_day) or \
                (birth_month == end_month and birth_day <= end_day)):
                return tree
    return None


def get_zodiac_sign(day, month):
    """
    Определяет знак зодиака на основе дня и месяца рождения.
    :param day: День рождения (int)
    :param month: Месяц рождения (int)
    :return: Название знака зодиака (str)
    """
    if (month == 3 and 21 <= day <= 31) or (month == 4 and 1 <= day <= 19):
        return "Овен"
    elif (month == 4 and 20 <= day <= 30) or (month == 5 and 1 <= day <= 20):
        return "Телец"
    elif (month == 5 and 21 <= day <= 31) or (month == 6 and 1 <= day <= 20):
        return "Близнецы"
    elif (month == 6 and 21 <= day <= 30) or (month == 7 and 1 <= day <= 22):
        return "Рак"
    elif (month == 7 and 23 <= day <= 31) or (month == 8 and 1 <= day <= 22):
        return "Лев"
    elif (month == 8 and 23 <= day <= 31) or (month == 9 and 1 <= day <= 22):
        return "Дева"
    elif (month == 9 and 23 <= day <= 30) or (month == 10 and 1 <= day <= 22):
        return "Весы"
    elif (month == 10 and 23 <= day <= 31) or (month == 11 and 1 <= day <= 21):
        return "Скорпион"
    elif (month == 11 and 22 <= day <= 30) or (month == 12 and 1 <= day <= 21):
        return "Стрелец"
    elif (month == 12 and 22 <= day <= 31) or (month == 1 and 1 <= day <= 19):
        return "Козерог"
    elif (month == 1 and 20 <= day <= 31) or (month == 2 and 1 <= day <= 18):
        return "Водолей"
    elif (month == 2 and 19 <= day <= 29) or (month == 3 and 1 <= day <= 20):
        return "Рыбы"
    else:
        return "Неизвестный знак"

def get_chinese_zodiac_animal(year):
    """
    Определяет животное по китайскому календарю на основе года рождения.
    :param year: Год рождения (int)
    :return: Название животного (str)
    """
    animals = [
        "Крыса", "Бык", "Тигр", "Кролик",
        "Дракон", "Змея", "Лошадь", "Коза",
        "Обезьяна", "Петух", "Собака", "Свинья"
    ]
    return animals[(year - 4) % 12]

def get_color_by_birthdate(birth_month):
    """
    Определяет цвет на основе месяца рождения.
    :param birth_month: Месяц рождения (int)
    :return: Цвет (str)
    """
    colors = [
        "Белый", "Синий", "Жёлтый", "Красный",
        "Розовый", "Голубой", "Золотой", "Коричневый",
        "Зелёный", "Оранжевый", "Чёрный", "Белый"
    ]
    return colors[(birth_month - 1) % 12]

def get_stone_by_birthdate(birth_day, birth_month):
    """
    Определяет камень на основе дня и месяца рождения.
    :param birth_day: День рождения (int)
    :param birth_month: Месяц рождения (int)
    :return: Название камня (str)
    """
    stones = {
        (1, 19): "Гранат", (20, 31): "Хризолит",  # Январь
        (1, 18): "Аметист", (19, 29): "Оникс",  # Февраль
        (1, 20): "Аквамарин", (21, 31): "Сапфир",  # Март
        (1, 19): "Алмаз", (20, 30): "Рубин",  # Апрель
        (1, 20): "Изумруд", (21, 31): "Топаз",  # Май
        (1, 20): "Жемчуг", (21, 30): "Александрит",  # Июнь
        (1, 22): "Карнеол", (23, 31): "Яшма",  # Июль
        (1, 22): "Сердолик", (23, 31): "Агат",  # Август
        (1, 22): "Сапфир", (23, 30): "Лазурит",  # Сентябрь
        (1, 22): "Опал", (23, 31): "Турмалин",  # Октябрь
        (1, 21): "Цитрин", (22, 30): "Малахит",  # Ноябрь
        (1, 21): "Танзанит", (22, 31): "Бирюза"  # Декабрь
    }

    for (start, end), stone in stones.items():
        if birth_month == 1 and birth_day >= start or birth_month == 12 and birth_day <= end:
            return stone
        elif birth_month != 1 and start <= birth_day <= end:
            return stone
    return "Неизвестный камень"

def get_element_by_zodiac(zodiac_sign):
    """
    Определяет стихию на основе знака зодиака.
    :param zodiac_sign: Знак зодиака (str)
    :return: Стихия (str)
    """
    elements = {
        "Овен": "Огонь",
        "Телец": "Земля",
        "Близнецы": "Воздух",
        "Рак": "Вода",
        "Лев": "Огонь",
        "Дева": "Земля",
        "Весы": "Воздух",
        "Скорпион": "Вода",
        "Стрелец": "Огонь",
        "Козерог": "Земля",
        "Водолей": "Воздух",
        "Рыбы": "Вода"
    }
    return elements.get(zodiac_sign, "Неизвестная стихия")


def get_planet_by_zodiac(zodiac_sign):
    """
    Определяет планету-покровителя на основе знака зодиака.
    :param zodiac_sign: Знак зодиака (str)
    :return: Планета (str)
    """
    planets = {
        "Овен": "Марс",
        "Телец": "Венера",
        "Близнецы": "Меркурий",
        "Рак": "Луна",
        "Лев": "Солнце",
        "Дева": "Меркурий",
        "Весы": "Венера",
        "Скорпион": "Плутон",
        "Стрелец": "Юпитер",
        "Козерог": "Сатурн",
        "Водолей": "Уран",
        "Рыбы": "Нептун"
    }
    return planets.get(zodiac_sign, "Неизвестная планета")


def get_life_path_number(birth_year, birth_month, birth_day):
    """
    Рассчитывает число судьбы на основе даты рождения.
    :param birth_year: Год рождения (int)
    :param birth_month: Месяц рождения (int)
    :param birth_day: День рождения (int)
    :return: Число судьбы (int)
    """
    digits = [int(digit) for digit in f"{birth_year}{birth_month:02d}{birth_day:02d}"]
    while sum(digits) >= 10:
        digits = [int(digit) for digit in str(sum(digits))]
    return sum(digits)


def get_totem_animal(birth_month):
    """
    Определяет тотемное животное на основе месяца рождения.
    :param birth_month: Месяц рождения (int)
    :return: Тотемное животное (str)
    """
    animals = [
        "Волк", "Медведь", "Ястреб", "Лиса", "Лев", "Олень",
        "Дельфин", "Лев", "Лиса", "Ворон", "Змея", "Сова"
    ]
    return animals[(birth_month - 1) % 12]