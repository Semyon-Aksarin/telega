import json
from pathlib import Path
import sqlite3

def load_zodiac_signs():
    """
    Загружает данные о знаках зодиака из JSON-файла.
    :return: Список словарей с информацией о знаках зодиака.
    """
    file_path = Path(__file__).parent / "static" / "zodiac_signs.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)["zodiac_signs"]

def drop_zodiac_signs_table():
    """
    Удаляет таблицу zodiac_signs, если она существует.
    """
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # SQL-запрос для удаления таблицы
    cursor.execute("DROP TABLE IF EXISTS zodiac_signs")

    connection.commit()
    connection.close()

def create_zodiac_signs_table():
    """
    Создаёт таблицу zodiac_signs в базе данных, если она не существует.
    """
    connection = sqlite3.connect('bot_database.db')
    cursor = connection.cursor()

    # SQL-запрос для создания таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zodiac_signs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        language TEXT NOT NULL,
        description TEXT NOT NULL,
        image_url TEXT,
        associated_trees TEXT
    )
    """)

    connection.commit()
    connection.close()

def add_zodiac_signs_to_db():
    """
    Добавляет данные о знаках зодиака в базу данных.
    """
    connection = sqlite3.connect('bot_database.db')
    cursor = connection.cursor()

    signs = load_zodiac_signs()
    for sign in signs:
        print(sign)  # Отладочный вывод для проверки данных
        cursor.execute("""
        INSERT INTO zodiac_signs (name, language, description, image_url, associated_trees)
        VALUES (?, ?, ?, ?, ?)
        """, (
            sign["name"],  # Используем "name" вместо "zodiac_sign"
            sign["language"],
            sign["description"],
            sign["image_url"],
            ", ".join(sign["associated_trees"])  # Преобразуем список деревьев в строку
        ))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    # Удаляем старую таблицу
    drop_zodiac_signs_table()

    # Создаём новую таблицу
    create_zodiac_signs_table()

    # Добавляем данные о знаках зодиака
    add_zodiac_signs_to_db()