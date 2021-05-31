import hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial
from PIL import ImageTk, Image
from database import *
import time
from tkinter import messagebox
import pyperclip
from encypt_decrypt import *

window = Tk()
photo = PhotoImage(file = "key.png")
window.iconphoto(False, photo)
window.title("My PassBook")
window.configure(bg='blue')
#window.wm_iconbitmap('key.png')


LABEL_FONT = ("Monospace", 12, "bold")
BUTTON_FONT = ("Sans-Serif", 10, "bold")
INFO_FONT = ("Verdana", 12)

#create popup
def popup(text): #text
    answer = simpledialog.askstring("input string", text)
    return answer

def hashpassword(pwd):
    hashpwd = hashlib.sha256(pwd.encode('utf-8'))
    hashpwd = hashpwd.hexdigest()

    return hashpwd

def signup():
    window.geometry("300x160")
    window.configure(bg='green')

    label1 = Label(window, text="Create Master Key", font=LABEL_FONT)
    label1.config(anchor=CENTER)
    label1.pack(pady=5)

    txt1 = Entry(window, width=20, show="*", font=INFO_FONT)
    txt1.pack(pady=1)
    txt1.focus()

    label2 = Label(window, text="Re-Enter Password", font=LABEL_FONT)
    label2.pack(pady=5)

    txt2 = Entry(window, width=20, show="*", font=INFO_FONT)
    txt2.pack(pady=1)
    txt2.focus()

    def savepassword():
        if txt1.get() == txt2.get():
            hashedPassword = hashpassword(txt1.get())
            savemasterpwd(hashedPassword)
            messagebox.showinfo(title='sign-up status', message="Master password is generated")
            vault()
        else:
            txt2.delete(0, 'end')
            messagebox.showerror(title='sign-up error', message="Password do not match.")

    button = Button(window, text="Create", command=savepassword, font=BUTTON_FONT)
    button.pack(pady=8)

def login():
    window.geometry("300x140")
    window.configure(bg='pink')

    label1 = Label(window, text = "Enter Master Key", font=LABEL_FONT)
    label1.config(anchor=CENTER)
    label1.pack(pady= 20)

    txt1 = Entry(window, width=20, show= "*", font=INFO_FONT)
    txt1.pack(pady= 5)
    txt1.focus()

    #label2 = Label(window, font=LABEL_FONT)
    #label2.pack()

    def getMasterKey():
        checkHashedPassword = hashpassword(txt1.get())
        pwd = getmasterpwd(checkHashedPassword)
        return pwd

    def check_password():
        password= getMasterKey()
        #print(password)

        if password:
            messagebox.showinfo(title='login status', message="logged in successfully")
            window.after(1500,vault())
        else:
            txt1.delete(0, 'end')
            #label2.config(text="wrong password")
            messagebox.showerror(title='login error', message="wrong password")

    button = Button(window, text = "Submit", command = check_password, font=BUTTON_FONT)
    button.pack(side= BOTTOM)

def vault():
    for widgets in window.winfo_children():
        widgets.destroy()
    window.configure(bg='grey')

    def addEntry():
        website = popup("Website")
        username1 = popup("Username")
        password1 = popup("Password")

        if (website == "") or (username1 == "") or (password1 == ""):
            messagebox.showerror(title='No data', message="please enter detail to proceed.")
            addEntry()
        else:
            password = encrypt_message(password1)
            username= encrypt_message(username1)
            savecredential(website, username, password)
            vault()

    def removeEntry(input):
        removecredential(input)
        vault()
        messagebox.showinfo(title='Deleted', message="Details removed from database.")

    def copytoclipboard(input):
        password = getpassword(input)
        password= decrypt_message(password[0][0])
        pyperclip.copy(password)
        return messagebox.showinfo(title='clipboard', message="password is copied to clipboard")

    def decrypt_password(input):
        password = getpassword(input)
        password = decrypt_message(password[0][0])
        return password

    def decrypt_username(input):
        username = getusername(input)
        username = decrypt_message(username[0][0])
        return username

    def delete():
        deletetable()
        vault()

    window.geometry("880x500")
    image = Image.open('key.png')
    # The (100, 100) is (height, width)
    image = image.resize((100, 100), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(image)

    label = Label(window, text= "My PassBook", font=LABEL_FONT, fg= 'orange',bg = 'black')
    label.grid(row=2, column=1)

    button1 = Button(window, text= "Add", command=addEntry, font=BUTTON_FONT, bg = 'blue', fg = 'white')
    button1.grid(row =2, column=0, pady = 20)

    button2 = Button(window, text="Delete All", command=delete, font=BUTTON_FONT, bg = 'blue', fg = 'white')
    button2.grid(row =2, column=2, pady=20 )

    label1 = Label(window, text= "Website/URL", font=LABEL_FONT, bg = 'red', fg = 'white')
    label1.grid(row=4, column= 0, padx=80, pady= 20)
    label2 = Label(window, text="Username", font=LABEL_FONT, bg = 'red', fg = 'white')
    label2.grid(row=4, column=1, padx=80, pady= 20)
    label3 = Label(window, text="Password", font=LABEL_FONT, bg = 'red', fg = 'white')
    label3.grid(row=4, column=2, padx=80, pady= 20)

    if (data_vault() != None):
        i = 0
        while True:
            array = data_vault()
            if (len(array) > i):
                #print(array)

                label4 = Label(window, text= (array[i][1]), font= ("Helvetica", 12), fg='yellow', bg = 'grey')
                label4.grid(column=0, row=i+5)
                label5 = Label(window, text=decrypt_username(array[i][0]), font= ("Helvetica", 12), fg='yellow', bg = 'grey')
                label5.grid(column=1, row=i + 5)
                label6 = Label(window, text=decrypt_password(array[i][0]) ,font= ("Helvetica", 12), fg='yellow', bg = 'grey')
                label6.grid(column=2, row=i + 5)

                button = Button(window, text="copy", font=BUTTON_FONT, bg = 'blue', fg = 'white', command= partial(copytoclipboard, array[i][0]))
                button.grid(column=4, row=i + 5, pady=10, padx=5)

                #button = Button(window, text="update", bg= "blue",  font=BUTTON_FONT, command=partial(update, array[i][0]))
                #button.grid(column=5, row=i + 4, pady=10, padx=5)

                button = Button(window, text="Delete", bg= "green", fg = 'white', font=BUTTON_FONT, command= partial(removeEntry, array[i][0]))
                button.grid(column=3, row = i+5,  pady =10 )

                i = i + 1
            else:
                break

#-------------------------------------------------------------#

if data_masterkey():
    login()
else:
    signup()

window.mainloop()