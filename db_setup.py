import sqlite3

conn = sqlite3.connect('app/database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        class TEXT,
        probability REAL
    )
''')

conn.commit()
conn.close()