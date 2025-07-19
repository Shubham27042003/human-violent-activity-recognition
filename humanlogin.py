import tkinter as tk  
from tkinter import ttk, LEFT, END
import sqlite3
from tkinter import messagebox as ms
from PIL import Image, ImageTk

# Setup main window
root = tk.Tk()
root.configure(background='white')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Login")

# Background image
image2 = Image.open('L4.png')  # Make sure this is a blue background image
image2 = image2.resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

# Variables
Email = tk.StringVar()
password = tk.StringVar()

# Functions
def reg():
    from subprocess import call
    call(["python", "human registration.py"])
    root.destroy()

def log():
    with sqlite3.connect('knee.db') as db:
        c = db.cursor()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS KneeReg"
                       "(name TEXT, address TEXT, Email TEXT, country TEXT, Phoneno TEXT, Gender TEXT, password TEXT)")
        db.commit()

        find_entry = 'SELECT * FROM KneeReg WHERE Email = ? AND password = ?'
        c.execute(find_entry, [(Email.get()), (password.get())])
        result = c.fetchall()
        if result:
            ms.showinfo("Message", "Login successfully")
            from subprocess import call
            call(['python', 'GUI_Master.py'])
        else:
            ms.showerror('Oops!', 'Username or Password did not match.')

def forgot():
    from subprocess import call
    call(['python', 'forgot password.py'])

# Position and style for the login box
box_width = 450
box_height = 350
center_x = (w - box_width) // 2
center_y = (h - box_height) // 2

# Login Canvas (Box)
canvas1 = tk.Canvas(root, background="#0c1f3f", highlightthickness=0)  # deep navy blue
canvas1.place(x=center_x, y=center_y, width=box_width, height=box_height)

# Labels and Entry Fields
tk.Label(root, text='Login Here', fg='white', bg='#1a2d5a', font=('Forte', 25)).place(x=center_x + 120, y=center_y - 40)

tk.Label(root, text='Enter Email', fg='white', bg='#0c1f3f', font=('Cambria', 14)).place(x=center_x + 30, y=center_y + 45)
tk.Entry(root, width=30, textvariable=Email).place(x=center_x + 170, y=center_y + 50)

tk.Label(root, text='Enter Password', fg='white', bg='#0c1f3f', font=('Cambria', 14)).place(x=center_x + 30, y=center_y + 95)
tk.Entry(root, width=30, show='*', textvariable=password).place(x=center_x + 170, y=center_y + 100)

# Buttons
tk.Button(root, text="Forgot Password?", fg='white', bg='#2e86de', command=forgot).place(x=center_x + 270, y=center_y + 150)

tk.Button(root, text="Log in", font=("Bold", 10), command=log, width=35, bg='#1abc9c', fg='white').place(x=center_x + 40, y=center_y + 200)

tk.Label(root, text='Not a Member?', font=('Cambria', 12), fg='white', bg='#0c1f3f').place(x=center_x + 120, y=center_y + 260)

tk.Button(root, text="Sign up", fg='white', bg='#2980b9', command=reg).place(x=center_x + 240, y=center_y + 260, width=55)

# Main loop
root.mainloop()
