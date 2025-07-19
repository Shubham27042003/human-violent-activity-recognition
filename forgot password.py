import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk

# ============ Main Window Setup ============ #
root = tk.Tk()
root.configure(background='white')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.title("Forget Password")

# ============ Background Image ============ #
try:
    image2 = Image.open('R3.png')  # Make sure R3.png exists in the same directory
    image2 = image2.resize((w, h), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0)
except Exception as e:
    ms.showerror("Image Error", f"Could not load background image.\n{e}")

# ============ Variables ============ #
email = tk.StringVar()
password = tk.StringVar()
confirmPassword = tk.StringVar()

# ============ Database Setup ============ #
db = sqlite3.connect('knee.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS KneeReg (
        name TEXT, 
        address TEXT,  
        Email TEXT PRIMARY KEY, 
        country TEXT, 
        Phoneno TEXT,
        Gender TEXT, 
        password TEXT
    )
''')
db.commit()
db.close()

# ============ Frame for Center Box ============ #
frame_width = 600
frame_height = 300
frame_x = (w - frame_width) // 2
frame_y = (h - frame_height) // 2

form_frame = tk.Frame(root, bg='#d0e7f9', bd=2, relief='ridge')  # Light blue background
form_frame.place(x=frame_x, y=frame_y, width=frame_width, height=frame_height)

# ============ Header ============ #
tk.Label(form_frame, text='Forgot Password', font=('Cambria', 18, 'bold'),
         bg='#d0e7f9', fg='black').pack(pady=(10, 20))

# ============ Input Fields ============ #
tk.Label(form_frame, text='Email', font=('Cambria', 14), bg='#d0e7f9').pack(anchor='w', padx=60)
tk.Entry(form_frame, width=40, textvariable=email).pack(pady=5)

tk.Label(form_frame, text='New Password', font=('Cambria', 14), bg='#d0e7f9').pack(anchor='w', padx=60)
tk.Entry(form_frame, width=40, show="*", textvariable=password).pack(pady=5)

tk.Label(form_frame, text='Confirm Password', font=('Cambria', 14), bg='#d0e7f9').pack(anchor='w', padx=60)
tk.Entry(form_frame, width=40, show="*", textvariable=confirmPassword).pack(pady=5)

# ============ Change Password Logic ============ #
def change_password():
    user_email = email.get().strip()
    new_pass = password.get().strip()
    confirm_pass = confirmPassword.get().strip()

    if not user_email or not new_pass or not confirm_pass:
        ms.showwarning("Incomplete", "Please fill all fields.")
        return

    if new_pass != confirm_pass:
        ms.showerror('Error', "Passwords didn't match!")
        return

    try:
        db = sqlite3.connect("knee.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM KneeReg WHERE Email = ?", (user_email,))
        result = cursor.fetchone()

        if result:
            cursor.execute("UPDATE KneeReg SET password = ? WHERE Email = ?", (new_pass, user_email))
            db.commit()
            ms.showinfo('Success', 'Password changed successfully.')
            root.destroy()
        else:
            ms.showerror("Not Found", "No account found with this email.")
    except Exception as e:
        ms.showerror("Database Error", str(e))
    finally:
        db.close()

# ============ Submit Button ============ #
tk.Button(form_frame, text="Submit", width=12, bg="#28b463", fg="white",
          font=('Cambria', 12, 'bold'), command=change_password).pack(pady=20)

# ============ Run App ============ #
root.mainloop()
