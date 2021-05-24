import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial
from database import *
import time
from tkinter import messagebox

window = Tk()
window.title("My PassBook")

#create popup
def popup(): #text
    #answer = simpledialog.askstring("input string", text)
    website = simpledialog.askstring("input string", "website")
    username = simpledialog.askstring("input string", "username")
    password = simpledialog.askstring("input string", "password")

    return website, username, password

def hashpassword(pwd):
    hashpwd = hashlib.md5(pwd)
    hashpwd = hashpwd.hexdigest()

    return hashpwd

def signup():
    window.geometry("300x140")

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
    label3.pack(pady=2)

    def savepassword():
        if txt1.get() == txt2.get():
            hashedPassword = hashpassword(txt1.get().encode('utf-8'))

            insert_password = """INSERT INTO masterkey(password) VALUES(?) """
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()
            messagebox.showinfo(title='sign-up status', message="Master password is generated")
            vault()
        else:
            txt2.delete(0, 'end')
            label3.config(text="No Match, please check the password")
            messagebox.showinfo(title='sign-up error', message="Password do not match.")

    button = Button(window, text="Create", command=savepassword)
    button.pack(pady=5)

def login():
    window.geometry("300x140")

    label1 = Label(window, text = "Enter Master Key")
    label1.config(anchor=CENTER)
    label1.pack()

    txt1 = Entry(window, width=20, show= "*")
    txt1.pack()
    txt1.focus()

    label2 = Label(window)
    label2.pack()

    def getMasterKey():
        checkHashedPassword = hashpassword(txt1.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterkey WHERE id=1 AND password = ?", [(checkHashedPassword)])
       #print(checkHashedPassword)
        return cursor.fetchall()

    def check_password():
        password= getMasterKey()
        #print(password)

        if password:
            window.after(1500,vault())
        else:
            txt1.delete(0, 'end')
            label3.destroy()
            label2.config(text="wrong password")

    label3 = Label(window, text='click to verify')
    label3.pack()

    button = Button(window, text = "Submit", command = check_password)
    button.pack()

def vault():
    for texts in window.winfo_children():
        texts.destroy()

    def addEntry():
        #text1 = "Website"
        #text2 = "Username"
        #text3 = "Password"

        website, username, password = popup()

        insert_fields = """INSERT INTO vault(website, username, password) VALUES(?, ?, ?) """

        cursor.execute(insert_fields, (website, username, password))
        db.commit()
        vault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id= ?", (input,))
        db.commit()
        vault()

    window.geometry("800x400")

    label = Label(window, text= "My PassBook")
    label.grid(column=1)

    button1 = Button(window, text="add", command=addEntry)
    button1.grid(column=1, pady=10)

    label1 = Label(window, text= "Website/URL")
    label1.grid(row=2, column= 0, padx=80)
    label2 = Label(window, text="Username")
    label2.grid(row=2, column=1, padx=80)
    label3 = Label(window, text="Password" )
    label3.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            label4 = Label(window, text= (array[i][1]), font= ("Helvetica", 12))
            label4.grid(column=0, row=i+3)
            label5 = Label(window, text=(array[i][2]), font= ("Helvetica", 12))
            label5.grid(column=1, row=i + 3)
            label6 = Label(window, text=(array[i][3]), font= ("Helvetica", 12))
            label6.grid(column=2, row=i + 3)

            button = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))
            button.grid(column=3, row = i+3,  pady =10)

            i= i+1

            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break



#-------------------------------------------------------------#


cursor.execute("SELECT * FROM masterkey")
if cursor.fetchall():
    login()
else:
    signup()

window.mainloop()
