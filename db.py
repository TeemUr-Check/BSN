import sqlite3
import os
from pathlib import Path

# Определяем путь к базе данных в папке проекта
DB_PATH = Path(__file__).parent / 'images.db'


def init_db():
    """Инициализация базы данных с явным указанием пути"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nickname TEXT NOT NULL,
                      action_type TEXT NOT NULL CHECK (action_type IN ('sell', 'exchange')),
                      image_data BLOB NOT NULL,
                      description TEXT NOT NULL,
                      contact TEXT NOT NULL,
                      title TEXT NOT NULL,
                      upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    print(f"База данных создана по пути: {DB_PATH}")


def save_book_data(nickname, action_type, image_file, description, contact, title):
    """Сохранение данных книги в БД"""
    try:
        image_data = image_file.read()
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO books 
                         (nickname, action_type, image_data, description, contact, title) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                       (nickname, action_type, image_data, description, contact, title))

        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False
    finally:
        conn.close()


def get_all_books():
    """Получение всех книг из БД"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY upload_date DESC")
    books = cursor.fetchall()
    conn.close()
    return books


if __name__ == '__main__':
    init_db()
