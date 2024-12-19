
import sqlite3

DATABASE = 'app.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                library_id INTEGER NOT NULL,
                FOREIGN KEY (library_id) REFERENCES library (id)
            )
        ''')
        conn.commit()

class User:
    @staticmethod
    def create(username, email, password):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_username(username):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
            return cursor.fetchone()

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user')
            return cursor.fetchall()

    @staticmethod
    def update(user_id, username, email):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE user SET username = ?, email = ? WHERE id = ?', (username, email, user_id))
            conn.commit()

    @staticmethod
    def delete(user_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
            conn.commit()

class Library:
    @staticmethod
    def create(name, user_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO library (name, user_id) VALUES (?, ?)', (name, user_id))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM library')
            return cursor.fetchall()

class Book:
    @staticmethod
    def create(title, author, library_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO book (title, author, library_id) VALUES (?, ?, ?)', (title, author, library_id))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM book')
            return cursor.fetchall()

    @staticmethod
    def update(book_id, title, author):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE book SET title = ?, author = ? WHERE id = ?', (title, author, book_id))
            conn.commit()

    @staticmethod
    def delete(book_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM book WHERE id = ?', (book_id,))
            conn.commit()