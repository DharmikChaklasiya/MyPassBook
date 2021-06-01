import sqlite3

#connection to DB called MyPassBook
with sqlite3.connect("MyPassBook.db") as db:
    cursor = db.cursor()

#creating table masterkey to store master password
cursor.execute("""
CREATE TABLE IF NOT EXISTS masterkey(
id INTEGER  PRIMARY KEY,
password TEXT NOT NULL);
""")

#creating table vault to store website, username and password
cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER  PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

#get all data from masterkey table
def data_masterkey():
    cursor.execute("SELECT * FROM masterkey")
    return cursor.fetchall()

#get all data from vault table
def data_vault():
    cursor.execute("SELECT * FROM vault")
    return cursor.fetchall()

#insert masterpassword to masterkey table
def savemasterpwd(input):
    insert_password = """INSERT INTO masterkey(password) VALUES(?) """
    cursor.execute(insert_password, [(input)])
    db.commit()

#get masterkey from table by comparing it
def getmasterpwd(input):
    cursor.execute("SELECT * FROM masterkey WHERE id=1 AND password = ?", [(input)])
    pwd = cursor.fetchall()
    return pwd

#insert inputs to table vault
def savecredential(url, user, pwd):
    insert_fields = """INSERT INTO vault(website, username, password) VALUES(?, ?, ?) """
    cursor.execute(insert_fields, (url, user, pwd))
    db.commit()

#get password from vault table using id
def getpassword(input):
    cursor.execute("SELECT password FROM vault WHERE id= ?", (input,))
    data = cursor.fetchall()
    db.commit()
    return data

#get username from vault table using id
def getusername(input):
    cursor.execute("SELECT username FROM vault WHERE id= ?", (input,))
    data = cursor.fetchall()
    db.commit()
    return data

#delete row by id from vault
def removecredential(input):
    cursor.execute("DELETE FROM vault WHERE id= ?", (input,))
    db.commit()

#delete everything from vault
def deletetable():
    cursor.execute("DELETE FROM vault")
    db.commit()

# def updatedata(input, user):
#     cursor.execute(f'''
#                        UPDATE vault
#                        SET username="{user}"
#                        WHERE id="{input}"''')
#     db.commit()



