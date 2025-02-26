import sqlite3

conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Создание таблицы users, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'ru',
            birth_year INTEGER,
            birth_month INTEGER,
            birth_day INTEGER,
            birth_hour INTEGER,
            birth_minute INTEGER,
            birthplace TEXT,
            zodiac_sign TEXT,                -- Новый столбец для знака зодиака
            chinese_zodiac_animal TEXT,      -- Новый столбец для животного
            tree TEXT,               -- Новый столбец для дерева
            stone TEXT,              -- Новый столбец для камня
            color TEXT,              -- Новый столбец для цвета
            element TEXT,            -- Новый столбец для стихии
            planet TEXT,             -- Новый столбец для планеты
            life_path_number INTEGER,-- Новый столбец для числа судьбы
            totem_animal TEXT        -- Новый столбец для тотемного животного
            balance	INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


def execute_query(query, params=()):
    connection = sqlite3.connect('bot_database.db')
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()  # Получаем все строки результата
        else:
            connection.commit()  # Фиксируем изменения для INSERT/UPDATE/DELETE
            result = None
    except Exception as e:
        print(f"Database error: {e}")
        result = None
    finally:
        connection.close()
    return result

# Получение данных пользователя
def get_user_data(user_id):
    """
    Получает данные пользователя из базы данных.
    :param user_id: ID пользователя (int)
    :return: Кортеж с данными пользователя или None, если пользователь не найден
    """
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id, language, birth_year, birth_month, birth_day,
               birth_hour, birth_minute, birthplace, zodiac_sign,
               chinese_zodiac_animal, tree, stone, color,
               element, planet, life_path_number, totem_animal
        FROM users
        WHERE user_id = ?
    ''', (user_id,))

    user_data = cursor.fetchone()
    conn.close()
    return user_data

# Сохранение данных пользователя
def save_user_data(user_id, data):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Проверяем, существует ли пользователь в базе
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone():
        # Обновляем существующие данные
        cursor.execute('''
            UPDATE users
            SET birth_year = ?, birth_month = ?, birth_day = ?, birth_hour = ?, birth_minute = ?,
                birthplace = ?, zodiac_sign = ?, chinese_zodiac_animal = ?, tree = ?, stone = ?, 
                color = ?, element = ?, planet = ?, life_path_number = ?, totem_animal = ?
            WHERE user_id = ?
        ''', (
            data.get('birth_year'),
            data.get('birth_month'),
            data.get('birth_day'),
            data.get('birth_hour'),
            data.get('birth_minute'),
            data.get('birthplace'),
            data.get('zodiac_sign'),  # Новое поле
            data.get('chinese_zodiac_animal'),  # Новое поле
            data.get('tree'),
            data.get('stone'),
            data.get('color'),
            data.get('element'),
            data.get('planet'),
            data.get('life_path_number'),
            data.get('totem_animal'),
            user_id
        ))
    else:
        # Вставляем новые данные
        cursor.execute('''
            INSERT INTO users (
                user_id, birth_year, birth_month, birth_day, birth_hour, birth_minute,
                birthplace, zodiac_sign, chinese_zodiac_animal, tree, stone, color, element, planet,
                life_path_number, totem_animal
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data.get('birth_year'),
            data.get('birth_month'),
            data.get('birth_day'),
            data.get('birth_hour'),
            data.get('birth_minute'),
            data.get('birthplace'),
            data.get('zodiac_sign'),  # Новое поле
            data.get('chinese_zodiac_animal'),  # Новое поле
            data.get('tree'),
            data.get('stone'),
            data.get('color'),
            data.get('element'),
            data.get('planet'),
            data.get('life_path_number'),
            data.get('totem_animal')
        ))

    conn.commit()
    conn.close()

def get_user_language(user_id):
    user_data = get_user_data(user_id)  # Получаем данные пользователя из базы
    if user_data and len(user_data) > 1:  # Проверяем, есть ли данные о языке
        return user_data[1]  # Второй элемент - язык
    else:
        return "ru"  # Язык по умолчанию

# Функция для сохранения языка пользователя
def save_user_language(user_id, language):
    cursor.execute("""
    INSERT INTO users (user_id, language)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        language = excluded.language
    """, (user_id, language))
    conn.commit()



