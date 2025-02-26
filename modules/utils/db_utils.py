from modules.database.db import execute_query

def get_text_from_db(language, key):
    query = "SELECT text FROM translations WHERE key = ? AND language = ?"
    result = execute_query(query, (key, language))
    if result:
        return result[0][0]  # Возвращаем текст из первой строки
    return None