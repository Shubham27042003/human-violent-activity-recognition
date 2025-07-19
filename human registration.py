import tkinter as tk
import sqlite3
import random
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import re

root = tk.Tk()
root.configure(background='white')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.title("Registration")

# Optional: set a background image resized to full screen (if you need this)
try:
    image2 = Image.open('r1.png')
    image2 = image2.resize((screen_width, screen_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0)
except Exception as e:
    print("Background image could not be loaded:", e)

# Registration form variables
name = tk.StringVar()
address = tk.StringVar()
Email = tk.StringVar()
country = tk.StringVar()
PhoneNo = tk.IntVar()
var = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()

value = random.randint(1, 1000)
print("Random value:", value)

# Database code (creating table if it doesn't exist)
db = sqlite3.connect('knee.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS KneeReg(
                   name TEXT, address TEXT, Email TEXT, country TEXT,
                   Phoneno TEXT, Gender TEXT, password TEXT)""")
db.commit()

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 6:
        print('Password length should be at least 6')
        val = False

    if len(passwd) > 20:
        print('Password length should not be greater than 20')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#%')
        val = False

    return val

def insert():
    fname = name.get()
    addr = address.get()
    un = country.get()
    email = Email.get()
    mobile = PhoneNo.get()
    gender = var.get()
    pwd = password.get()
    cnpwd = password1.get()

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    valid_email = True if re.search(regex, email) else False

    if (fname.isdigit() or (fname == "")):
        ms.showinfo("Message", "Please enter a valid name")
    elif (addr == ""):
        ms.showinfo("Message", "Please enter an address")
    elif (email == "") or (not valid_email):
        ms.showinfo("Message", "Please enter a valid email")
    elif (len(str(mobile)) != 10):
        ms.showinfo("Message", "Please enter a 10 digit mobile number")
    elif (un == ""):
        ms.showinfo("Message", "Please enter a valid country")
    elif (pwd == ""):
        ms.showinfo("Message", "Please enter a valid password")
    elif (pwd == "" or not password_check(pwd)):
        ms.showinfo("Message", "Password must contain at least one uppercase letter, one symbol, and one number")
    elif (pwd != cnpwd):
        ms.showinfo("Message", "Password and Confirm Password must be the same")
    else:
        conn = sqlite3.connect('knee.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO KneeReg(name, address, Email, country, Phoneno, Gender, password) VALUES(?,?,?,?,?,?,?)',
                (fname, addr, email, un, mobile, gender, pwd))
            conn.commit()
            db.close()
            ms.showinfo('Success!', 'Account Created Successfully!')
            # Switch to login window if needed
            from subprocess import call
            call(['python', 'human GUI_Main.py'])

# -----------------------
# Centering the Registration Box
# -----------------------
# Define registration box dimensions (canvas size)
reg_box_width = 400
reg_box_height = 590

# Compute offsets to center the registration box on the screen
offset_x = (screen_width - reg_box_width) // 2
offset_y = (screen_height - reg_box_height) // 2

# Place header label above the registration box
header_label = tk.Label(root, text="Registration Form", font=("Forte", 30), fg="black", bg="white")
# Position header centered horizontally (optional offset, here 0 means centered based on its own width)
header_label.place(x=offset_x + (reg_box_width // 2) - 155, y=offset_y - 60)

# Create a canvas to act as the registration form container
canvas = tk.Canvas(root, background="black", borderwidth=0)
canvas.place(x=offset_x, y=offset_y, width=reg_box_width, height=reg_box_height)

# Define field starting positions relative to the registration box (canvas)
field_label_x = offset_x + 50      # label x position inside the canvas
field_entry_x = offset_x + 200     # entry x position inside the canvas

# Y positions for each field (adjust these values as needed)
y_name = offset_y + 50
y_email = offset_y + 100
y_password = offset_y + 150
y_repassword = offset_y + 200
y_address = offset_y + 250
y_country = offset_y + 300
y_phone = offset_y + 350
y_gender = offset_y + 400

# Form: Name
tk.Label(root, text="Name:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_name)
tk.Entry(root, border=2, textvariable=name).place(x=field_entry_x, y=y_name + 5)

# Form: Email
tk.Label(root, text="Email:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_email)
tk.Entry(root, border=2, textvariable=Email).place(x=field_entry_x, y=y_email + 5)

# Form: Password
tk.Label(root, text="Password:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_password)
tk.Entry(root, border=2, show="*", textvariable=password).place(x=field_entry_x, y=y_password + 5)

# Form: Re-Enter Password
tk.Label(root, text="Re-Enter Password:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_repassword)
tk.Entry(root, border=2, show="*", textvariable=password1).place(x=field_entry_x, y=y_repassword + 5)

# Form: Address
tk.Label(root, text="Address:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_address)
tk.Entry(root, border=2, textvariable=address).place(x=field_entry_x, y=y_address + 5)

# Form: Country
tk.Label(root, text="Country:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_country)
tk.Entry(root, border=2, textvariable=country).place(x=field_entry_x, y=y_country + 5)

# Form: Phone Number
tk.Label(root, text="Phone no:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_phone)
tk.Entry(root, border=2, textvariable=PhoneNo).place(x=field_entry_x, y=y_phone + 5)

# Form: Gender
tk.Label(root, text="Gender:", font=("Calibri", 14), bg="black", fg="white").place(x=field_label_x, y=y_gender)
tk.Radiobutton(root, text="Male", font=("Calibri", 14), bg="white", value=1, variable=var).place(x=field_entry_x, y=y_gender)
tk.Radiobutton(root, text="Female", font=("Calibri", 14), bg="white", value=2, variable=var).place(x=field_entry_x + 100, y=y_gender)

# Create Account Button
btn = tk.Button(root, text="Create Account", font=("Arial", 12), width=20, command=insert,
                bg="#5499c7", fg="white")
btn.place(x=offset_x + (reg_box_width // 2) - 100, y=y_gender + 60)

# Already have an account label and login button
tk.Label(root, text="Already have an account? ", bg="white", font=('Cambria', 11)) \
    .place(x=offset_x + (reg_box_width // 2) - 70, y=y_gender + 110)

def reg():
    from subprocess import call
    call(['python', 'humanlogin.py'])

button1 = tk.Button(root, text="Log in", fg='blue', bg='white', command=reg)
button1.place(x=offset_x + (reg_box_width // 2) + 120, y=y_gender + 110)

root.mainloop()
