import sqlite3


with sqlite3.connect("MyPassBook.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterkey(
id INTEGER  PRIMARY KEY,
password TEXT NOT NULL);
""")
