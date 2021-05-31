import sqlite3

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
def data_masterkey():
    cursor.execute("SELECT * FROM masterkey")
    return cursor.fetchall()

def data_vault():
    cursor.execute("SELECT * FROM vault")
    return cursor.fetchall()

def savemasterpwd(input):
    insert_password = """INSERT INTO masterkey(password) VALUES(?) """
    cursor.execute(insert_password, [(input)])
    db.commit()

def getmasterpwd(input):
    cursor.execute("SELECT * FROM masterkey WHERE id=1 AND password = ?", [(input)])
    pwd = cursor.fetchall()
    return pwd

def savecredential(url, user, pwd):
    insert_fields = """INSERT INTO vault(website, username, password) VALUES(?, ?, ?) """
    cursor.execute(insert_fields, (url, user, pwd))
    db.commit()

def getpassword(input):
    cursor.execute("SELECT password FROM vault WHERE id= ?", (input,))
    data = cursor.fetchall()
    db.commit()
    return data

def getusername(input):
    cursor.execute("SELECT username FROM vault WHERE id= ?", (input,))
    data = cursor.fetchall()
    db.commit()
    return data

def removecredential(input):
    cursor.execute("DELETE FROM vault WHERE id= ?", (input,))
    db.commit()

def deletetable():
    cursor.execute("DELETE FROM vault")
    db.commit()
# def updatedata(input, user):
#     cursor.execute(f'''
#                        UPDATE vault
#                        SET username="{user}"
#                        WHERE id="{input}"''')
#     db.commit()



