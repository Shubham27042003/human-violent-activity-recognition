import tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import os

# ======================== MAIN WINDOW CONFIG ======================== #
root = tk.Tk()
root.title("Human Violence Activity Recognization")
root.configure(background="skyblue")

# Set full screen window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")

# ======================== BACKGROUND IMAGE ======================== #
try:
    image2 = Image.open("s3.png")
    image2 = image2.resize((w, h), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)

    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image  # Prevent garbage collection
    background_label.place(x=0, y=0)
except Exception as e:
    ms.showerror("Image Error", f"Could not load background image.\n{str(e)}")

# ======================== BUTTON FUNCTIONS ======================== #
def log():
    from subprocess import call
    call(["python", "humanlogin.py"])

def reg():
    from subprocess import call
    call(["python", "human registration.py"])

def window():
    root.destroy()

# ======================== BUTTON STYLES ======================== #
button_style = {
    "width": 12,
    "height": 1,
    "font": ('Times', 20, 'bold'),
    "bg": "#2E86C1",               # Blue matching sky
    "fg": "white",
    "activebackground": "#1A5276", # Slightly darker on hover
    "activeforeground": "white"
}

# ======================== BUTTON PLACEMENT ======================== #
tk.Button(root, text="Login", command=log, **button_style).place(x=100, y=500)
tk.Button(root, text="Register", command=reg, **button_style).place(x=400, y=500)
tk.Button(
    root, text="Exit", command=window,
    **{**button_style, "bg": "#C0392B", "activebackground": "#922B21"}  # Red Exit button
).place(x=700, y=500)

# ======================== MAINLOOP ======================== #
root.mainloop()
