import sqlite3
import hashlib
from tkinter import *
from database import *
import time


window = Tk()

window.title("My PassBook")

def hashpassword():
    pass


def signup():
    window.geometry("250x150")

    label1 = Label(window, text="Create Master Key")
    label1.config(anchor=CENTER)
    label1.pack()

    txt1 = Entry(window, width=20, show="*")
    txt1.pack()
    txt1.focus()

    label2 = Label(window, text="Re-Enter Password")
    label2.pack()

    txt2 = Entry(window, width=20, show="*")
    txt2.pack()
    txt2.focus()

    label3 = Label(window)
    label3.pack(pady=4)

    def savepassword():
        if txt1.get() == txt2.get():
            hashedPassword = txt1.get()

            insert_password = """INSERT INTO masterkey(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()

            vault()
        else:
            label3.config(text="No Match, please check the password")

    button = Button(window, text="Create", command=savepassword)
    button.pack(pady=10)

def login():
    window.geometry("250x150")

    label1 = Label(window, text = "Enter Master Key")
    label1.config(anchor=CENTER)
    label1.pack()

    txt1 = Entry(window, width=20, show= "*")
    txt1.pack()
    txt1.focus()

    label2 = Label(window)
    label2.pack()

    def getMasterKey():
        checkHashedPassword = txt1.get()
        cursor.execute("SELECT * FROM masterkey WHERE id=1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    def check_password():
        password= getMasterKey()

        if password:
            label3.config(text="verify")
            #label3['text'] = 'Wait for it...'
            window.after(2000, vault())
        else:
            txt1.delete(0, 'end')
            label2.config(text="wrong password")

    label3 = Label(window)
    label3.pack(pady=1)

    button = Button(window, text = "Submit", command = check_password)
    button.pack(pady=3)

def vault():
    for texts in window.winfo_children():
        texts.destroy()

    window.geometry("800x400")

    label = Label(window, text= "My PassBook")
    label.config(anchor=CENTER)
    label.pack()

cursor.execute("SELECT * FROM masterkey")
if cursor.fetchall():
    login()
else:
    signup()

window.mainloop()
