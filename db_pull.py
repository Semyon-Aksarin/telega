import pandas as pd
import aiosqlite
import numpy as np
from pathlib import Path
import asyncio


import asyncio
from pathlib import Path

# Function to ensure the table exists
async def ensure_table_exists(db_path):
    """
    Ensures the translations table exists in the database.
    :param db_path: Path to the SQLite database file.
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT,
                key TEXT NOT NULL,
                language TEXT NOT NULL,
                text TEXT,
                short_description TEXT,
                full_description TEXT,
                image_url TEXT,
                UNIQUE(key, language)
            )
        """)
        await db.commit()
        print("[DEBUG] Table 'translations' ensured.")

# Main function to execute the script logic
async def main():
    """
    Main asynchronous function to execute the script logic.
    """
    # Path to the database
    db_path = Path(__file__).resolve().parents[2] / "PycharmProjects/telega3/bot_database.db"

    # Ensure the table exists
    await ensure_table_exists(db_path)

    # Add your additional logic here (e.g., adding translations from Excel)
    excel_file_path = "translations.xlsx"
    try:
        await add_translations_from_excel(excel_file_path)
    except Exception as e:
        print(f"[ERROR] An error occurred while adding translations: {e}")

# Run the async function using asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())


async def add_translations_from_excel(file_path: str):
    """
    Добавляет или обновляет переводы в таблице `translations` из Excel-файла.
    :param file_path: Путь к Excel-файлу.
    """
    # Чтение Excel-файла
    try:
        # Чтение Excel-файла
        df = pd.read_excel(file_path)

        # Замена nan на None (или пустые строки '')
        df = df.replace({np.nan: None})  # Или df = df.replace({np.nan: ''})
    except Exception as e:
        print(f"[ERROR] Ошибка при чтении Excel-файла: {e}")
        return

    # Путь к базе данных
    db_path = Path(__file__).resolve().parents[2] / "PycharmProjects/telega3/bot_database.db"

    # Подключение к базе данных
    try:
        async with aiosqlite.connect(db_path) as db:
            # Получаем список колонок из таблицы `translations`
            async with db.execute("PRAGMA table_info(translations)") as cursor:
                columns = [row[1] for row in await cursor.fetchall()]

            # Обрабатываем каждую строку из Excel
            for _, row in df.iterrows():
                # Формируем словарь значений для записи в БД
                data = {col: row.get(col) for col in columns if col in row}
                print(f"[DEBUG] Данные для вставки: {data}")

                # Проверяем, существует ли запись с такими же `key` и `language`
                async with db.execute(
                    "SELECT id FROM translations WHERE key = ? AND language = ?",
                    (data.get("key"), data.get("language"))
                ) as cursor:
                    existing_record = await cursor.fetchone()

                if existing_record:
                    # Обновляем существующую запись
                    set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
                    values = list(data.values()) + [data["key"], data["language"]]
                    await db.execute(
                        f"UPDATE translations SET {set_clause} WHERE key = ? AND language = ?",
                        values
                    )
                else:
                    # Создаем новую запись
                    columns_str = ", ".join(data.keys())
                    placeholders = ", ".join(["?"] * len(data))
                    await db.execute(
                        f"INSERT INTO translations ({columns_str}) VALUES ({placeholders})",
                        list(data.values())
                    )

            # Сохраняем изменения
            await db.commit()
            print("[DEBUG] Переводы успешно добавлены/обновлены в таблице `translations`.")
    except Exception as e:
        print(f"[ERROR] Ошибка при работе с базой данных: {e}")


# Путь к Excel-файлу
excel_file_path = "translations.xlsx"

# Вызов функции через asyncio.run()
if __name__ == "__main__":
    asyncio.run(add_translations_from_excel(excel_file_path))