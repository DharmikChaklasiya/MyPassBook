import sqlite3
from tkinter import simpledialog

with sqlite3.connect("MyPassBook.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterkey(
id INTEGER  PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER  PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")


