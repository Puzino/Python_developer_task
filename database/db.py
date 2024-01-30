# SQLite3 Connection file
import sqlite3


class SqlDB:
    def __init__(self):  # Initialization of base fields
        self._connection = sqlite3.connect('db.sqlite3')
        self._cursor = self._connection.cursor()

    def create_table(self):  # Create or get table
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                location TEXT NULL DEFAULT NULL,
                feedback TEXT NULL DEFAULT NULL,
                comment TEXT NULL DEFAULT NULL,
                photo TEXT NULL DEFAULT NULL,
                openai_response TEXT NULL DEFAULT NULL
            );
            """)

    # Add fields to database
    def add_to_database(self, user_id, location, feedback, comment, photo, openai_response):
        self._cursor.execute(
            'INSERT INTO Users (user_id, location, feedback, comment, photo) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, location, feedback, comment, photo, openai_response))
        self._commit()

    def _commit(self):  # Save changes
        self._connection.commit()

    def close_connection(self):  # Close sql connection
        self._connection.close()
