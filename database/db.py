import sqlite3


class SqlDB:
    def __init__(self):
        # Инициализация базовых значений
        self._connection = sqlite3.connect('db.sqlite3')
        self._cursor = self._connection.cursor()

    # Создание/Получение таблицы
    def create_table(self):
        # Создаем таблицу Users
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            location TEXT NULL DEFAULT NUll,
            feedback TEXT NULL DEFAULT NUll,
            comment TEXT NULL DEFAULT NUll,
            photo TEXT NULL DEFAULT NUll)
            """)

    # Добавление в базу
    def add_to_database(self, user_id, location, feedback, comment, photo):
        self._cursor.execute(
            'INSERT INTO Users (user_id, location, feedback, comment, photo) VALUES (?, ?, ?, ?, ?)',
            (user_id, location, feedback, comment, photo))
        self._commit()

    # Сохраняем изменения
    def _commit(self):
        self._connection.commit()

    # Закрываем соединение
    def close_connection(self):
        self._connection.close()
