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

"""create popup"""
def popup(text):  # text
    """a pop will be open asking for input and return it."""
    answer = simpledialog.askstring("input string", text)
    return answer


"""hash function for master password"""
def hashpassword(pwd):
    """ it will take hash it with sha256(secure hash algo) function """
    hashpwd = hashlib.sha256(pwd.encode('utf-8'))  # encode convert strings to bytes
    hashpwd = hashpwd.hexdigest()  # internal block size of digest is 32 bits
    return hashpwd  # retuen one way hash value


"""signup window"""
def signup():
    # creates display of given size and bg set it to blue
    window.geometry("300x160")
    #max size of window set by "330X180"
    window.maxsize(330, 180)
    #configure window background to green coclor
    window.configure(bg='green')

    """Labels and text entries asking to create a Masterkey"""
    label1 = Label(window, text="Create MasterKey:", font=LABEL_FONT)
    # label1.config(anchor=CENTER)
    label1.pack(pady=5)

    txt1 = Entry(window, width=20, show="*", font=INFO_FONT)  # show=* will hide text with *
    txt1.pack(pady=1)
    txt1.focus()  # Place cursor into txt1 Entry

    label2 = Label(window, text="Re-Enter MasterKey:", font=LABEL_FONT)
    label2.pack(pady=5)

    txt2 = Entry(window, width=20, show="*", font=INFO_FONT)
    txt2.pack(pady=1)

    """Function to save inserted Masterkey"""
    def savepassword():
        ''' if inserted password in both entry matches then it will hash
        the password and save it database table called masterkey using
        function savemasterpwd() from databse.py else it will ask to enter passwords again'''
        if txt1.get() and txt2.get():
            if txt1.get() == txt2.get():
                hashedPassword = hashpassword(txt1.get())  # get():Returns the entry's current text as a string
                # calling function from DB to save it
                savemasterpwd(hashedPassword)
                # confirmation message box will pop up
                messagebox.showinfo(title='sign-up status', message="Master password is generated")
                # will redirect to home page called vault
                vault()
            else:
                txt2.delete(0, 'end')  # delete text from box
                # error pop ups
                messagebox.showerror(title='sign-up error', message="Password do not match.")
        else:
            txt1.focus()
            messagebox.showerror(title='No Text entered', message="please enter details to proceed.")

    button = Button(window, text="Create", command=savepassword, font=BUTTON_FONT)  # onclick savepassword() will be called
    button.pack(pady=8)


def is_master_password(pwd):
    """ Hashes the given password and check whether it matches the master password in the DB,
        returns True if matches else returns False. """
    hashedPassword = hashpassword(pwd)
    return bool(getmasterpwd(hashedPassword))


"""Login window"""
def login():
    # creates display of given size and bg set it to pink
    window.geometry("300x140")
    window.maxsize(330, 160)
    window.configure(bg='pink')

    """Labels and text entries asking to enter a Masterkey"""
    label1 = Label(window, text="Enter Master Key", font=LABEL_FONT)
    label1.config(anchor=CENTER)
    label1.pack(pady=20)

    txt1 = Entry(window, width=20, show="*", font=INFO_FONT)
    txt1.pack(pady=5)
    txt1.focus()  # Place cursor into name Entry

    # label2 = Label(window, font=LABEL_FONT)
    # label2.pack()

    '''function to check if master key is correct'''
    def check_password():
        ''' if there was match and getmasterkey() return some values
        then it will be redirected to main home page(vault)'''
        if is_master_password(txt1.get()):
            messagebox.showinfo(title='login status', message="logged in successfully")
            window.after(1500, vault())  # time= 1500 ms; it delays window to load with that time
        else:
            # else error will pop up
            txt1.delete(0, 'end')
            # label2.config(text="wrong password")
            messagebox.showerror(title='login error', message="wrong password")

    button = Button(window, text="Submit", command=check_password,font=BUTTON_FONT)  # on click check_password() will be called
    button.pack(pady=5)

'''funvtion to decrypt retrieved password from DB'''
def decrypt_password(input):
    password = getpassword(input)               #get password from DB using id input
    password = decrypt_message(password[0][0])  #decrypt retrived password using decrpt_message() function
    return password

'''funvtion to decrypt retrieved username from DB'''
def decrypt_username(input):
    username = getusername(input)               #get username from DB using id input
    username = decrypt_message(username[0][0])  #decrypt retrived username using decrpt_message() function
    return username

'''function to display main screen(Home Screen)'''
def vault():
    #Return a list of all widgets which are children of windows.
    for widgets in window.winfo_children():
        #destroy all widgets from the list
        widgets.destroy()
    window.configure(bg='grey')

    '''function to Insert data'''
    def addEntry():
        '''calling popup() function to ask to enter website, username, password'''
        website = popup("Website")
        username1 = popup("Username")
        password1 = popup("Password")

        #on clicking close button it will return none values so if values are not none then it will process.
        if website and username1 and password1:
            #check if user enetered details or not, if not details entered then error will pop up and ask again to add data
            if (website == "") or (username1 == "") or (password1 == ""):
                messagebox.showerror(title='No data', message="please enter detail to proceed.")
                addEntry()
            else:
                #else it will encrypt inserted password and username
                password = encrypt_message(password1)
                username = encrypt_message(username1)
                #and data will be stored in DB using function savecredential()
                savecredential(website, username, password)
                # will reload home screen for any changes
                vault()
    '''function to delete particular credential'''
    def removeEntry(input):
        #by calling removecredential(), row will be deleted using that credential id from DB
        removecredential(input)
        vault()
        #confermation pop up
        messagebox.showinfo(title='Deleted', message="Details removed from database.")

    '''function to copy password'''
    def copytoclipboard(input):
        #retrive password from DB using id
        password = getpassword(input)
        #decrypt pwd
        password = decrypt_message(password[0][0])
        #pyperclip is module to copy or paste clipboard
        pyperclip.copy(password)
        #return confirmation that pwd is copied to clipboard
        return messagebox.showinfo(title='clipboard', message="password is copied to clipboard")

    '''function to delete all data at once'''
    def delete():
        #check if there is alredy data stored if yes then it will ask to confirm master pwd
        if data_vault():
            #hash the entered master key
            masterkey = hashpassword(popup("Enter Masterkey:"))
            #check the entered master key if it found in DB then it will process
            if getmasterpwd(masterkey):
                #by calling function deletetable() from DB it will delete all stored data
                deletetable()
                # and refresh the page
                vault()
                #confirmation will pop up
                messagebox.showinfo(title='Delete', message="All data removed")
        else:
            #if there is no data stored yet then error will pop up
            messagebox.showerror(title='No data', message="there's no data stored.")

    '''window screen configuration'''
    window.geometry("880x500")
    window.maxsize(900, 600)
    #image = Image.open('images/key.png')
    # The (100, 100) is (height, width)
    #image = image.resize((100, 100), Image.ANTIALIAS)
    #my_img = ImageTk.PhotoImage(image)

    label = Label(window, text="My PassBook", font=LABEL_FONT, fg='orange', bg='black')
    label.grid(row=2, column=1)

    button1 = Button(window, text="Add", command=addEntry, font=BUTTON_FONT, bg='blue', fg='white')
    button1.grid(row=2, column=0, pady=20)

    button2 = Button(window, text="Delete All", command=delete, font=BUTTON_FONT, bg='blue', fg='white')
    button2.grid(row=2, column=2, pady=20)

    label1 = Label(window, text="Website/URL", font=LABEL_FONT, bg='red', fg='white')
    label1.grid(row=4, column=0, padx=80, pady=20)
    label2 = Label(window, text="Username", font=LABEL_FONT, bg='red', fg='white')
    label2.grid(row=4, column=1, padx=80, pady=20)
    label3 = Label(window, text="Password", font=LABEL_FONT, bg='red', fg='white')
    label3.grid(row=4, column=2, padx=80, pady=20)

    #if data in vault table is not none
    if (data_vault() != None):
        i = 0
        #loop will continue working till it will not be break
        while True:
            #storing all data from vault table to array
            array = data_vault()
            #loop should work till length of array is bigger then varible i
            if (len(array) > i):
                # print(array)

                #array[i][1] == website
                label4 = Label(window, text=(array[i][1]), font=("Helvetica", 12), fg='yellow', bg='grey')
                label4.grid(column=0, row=i + 5)
                #array[i][0] == id
                #decrypt_username will retrive username using that id and decrypt it
                label5 = Label(window, text=decrypt_username(array[i][0]), font=("Helvetica", 12), fg='yellow', bg='grey')
                label5.grid(column=1, row=i + 5)
                # decrypt_password will retrive password using that id and decrypt it
                label6 = Label(window, text=decrypt_password(array[i][0]), font=("Helvetica", 12), fg='yellow', bg='grey')
                label6.grid(column=2, row=i + 5)

                '''partial from functools pass the argument to command in our case it's id'''
                #button for copy password
                button = Button(window, text="copy", font=BUTTON_FONT, bg='blue', fg='white',command=partial(copytoclipboard, array[i][0]))
                button.grid(column=4, row=i + 5, pady=10, padx=5)

                # button = Button(window, text="update", bg= "blue",  font=BUTTON_FONT, command=partial(update, array[i][0]))
                # button.grid(column=5, row=i + 4, pady=10, padx=5)

                # button for copy password
                button = Button(window, text="Delete", bg="green", fg='white', font=BUTTON_FONT,command=partial(removeEntry, array[i][0]))
                button.grid(column=3, row=i + 5, pady=10)

                #after every iteration increase i by one
                i = i + 1
            else:
                #if length of array is not bigger then varible i anymore then it will break the loop
                break


# -------------------------------------------------------------#
#main method
if __name__ == '__main__':
    global window
    window = Tk()

    # adding icon for window display
    photo = PhotoImage(file="images/key.png")
    window.iconphoto(False, photo)

    #title set to "My PassBook"
    window.title("My PassBook")
    # set background coclor to blue
    window.configure(bg='blue')

    """setting basic fonts styles"""
    LABEL_FONT = ("Monospace", 12, "bold")
    BUTTON_FONT = ("Sans-Serif", 10, "bold")
    INFO_FONT = ("Verdana", 12)

    '''if master key exist then start with login window else ask user to create one by starting with signup window'''
    if data_masterkey():
        login()
    else:
        signup()

    window.mainloop()