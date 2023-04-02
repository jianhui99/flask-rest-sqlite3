import sqlite3

conn = sqlite3.connect('books.sqlite3')

cursor = conn.cursor()
sql_query = """CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    read INTEGER NOT NULL
)"""

cursor.execute(sql_query)

conn.commit()

conn.close()


