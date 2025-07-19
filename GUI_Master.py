# -- All imports --
import tkinter as tk
from PIL import Image, ImageTk
import time
import numpy as np
import cv2
from tkinter.filedialog import askopenfilename
import smtplib
from email.message import EmailMessage
import imghdr
import threading
import os
from playsound import playsound
from collections import deque
import Train_FDD_cnn as TrainM

# -- Main GUI Setup --
root = tk.Tk()
root.state('zoomed')
root.title("Human Violence Detection System")
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# -- Background --
try:
    bg_image = Image.open("bg.jpeg").resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    tk.Label(root, image=bg_photo).place(x=0, y=0)
except Exception as e:
    print("Background image error:", e)

# -- Title --
title = tk.Label(root, text="INTELLIGENT VIDEO SURVEILLANCE SYSTEM", font=("Times New Roman", 32, "bold"),
                 bg="black", fg="white", pady=20)
title.pack(fill=tk.X)

# -- Video Display Frame --
video_frame = tk.Frame(root, width=screen_width, height=screen_height, bg="black", bd=4, relief="ridge")
video_frame.place(x=0, y=0)
video_label = tk.Label(video_frame, bg="black")
video_label.pack(fill="both", expand=True)

btn_close_video = tk.Button(video_frame, text="❌ Close Video", font=("Arial", 16, "bold"), bg="red", fg="white")

result_label = tk.Label(root, text="", font=("Arial", 16), bg="black", fg="white")
result_label.place(x=20, y=screen_height - 40)

# -- Button Style & Buttons --
btn_style = {"font": ("Times New Roman", 24, "bold"), "width": 20, "pady": 10}

btn_detect = tk.Button(root, text="📹 Violence Detection",
                       command=lambda: threading.Thread(target=video_verify, daemon=True).start(),
                       bg="cyan", fg="black", **btn_style)
btn_detect.place(x=screen_width // 2 + 100, y=screen_height // 2 - 100)

btn_webcam = tk.Button(root, text="📷 Real-Time Detection",
                       command=lambda: threading.Thread(target=start_webcam_detection, daemon=True).start(),
                       bg="green", fg="white", **btn_style)
btn_webcam.place(x=screen_width // 2 + 100, y=screen_height // 2)

btn_exit = tk.Button(root, text="❌ Exit", command=root.destroy,
                     bg="red", fg="white", **btn_style)
btn_exit.place(x=screen_width // 2 + 100, y=screen_height // 2 + 100)

# -- UI Helpers --
def hide_ui():
    title.pack_forget()
    btn_detect.place_forget()
    btn_webcam.place_forget()
    btn_exit.place_forget()
    result_label.place_forget()

def show_ui():
    title.pack(fill=tk.X)
    btn_detect.place(x=screen_width // 2 + 100, y=screen_height // 2 - 100)
    btn_webcam.place(x=screen_width // 2 + 100, y=screen_height // 2)
    btn_exit.place(x=screen_width // 2 + 100, y=screen_height // 2 + 100)
    result_label.place(x=20, y=screen_height - 40)

# -- Email Alert --
def mail():
    try:
        sender = "pragati.code@gmail.com"
        receiver = "shubhams2504@gmail.com"
        password = "grqheqzoutabdfzd"
        msg = EmailMessage()
        msg['Subject'] = "⚠️ Violence Detected - Immediate Attention Required"
        msg['From'] = sender
        msg['To'] = receiver

        if not os.path.exists('abc.png'):
            print("Image file not found.")
            return

        with open('abc.png', 'rb') as f:
            img_data = f.read()
            img_type = imghdr.what(f.name)
            img_name = os.path.basename(f.name)

        msg.set_content("A violent activity has been detected. Please check the attached image.")
        msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Alert email sent.")
    except Exception as e:
        print("Failed to send email:", e)

# -- Buzzer Alert --
def play_alert():
    try:
        playsound("alert.mp3")
    except Exception as e:
        print("Error playing alert sound:", e)

# -- Result Message --
def update_label(message):
    result_label.config(text=message)
    result_label.after(5000, lambda: result_label.config(text=""))

# -- Real-Time Detection Function --
def start_webcam_detection():
    from tensorflow.keras.models import load_model
    global stop_video_flag
    stop_video_flag = False

    try:
        model = load_model('train_model.h5', compile=False)
    except Exception as e:
        update_label(f"❌ Failed to load model: {e}")
        return

    cap = cv2.VideoCapture(0)
    alert_active = False
    cooldown_counter = 0
    cooldown_frames = 10
    pred_queue = deque(maxlen=10)
    confidence_threshold = 0.4
    img_size = (224, 224)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    hide_ui()

    def close_webcam():
        global stop_video_flag
        stop_video_flag = True
        cap.release()
        video_label.config(image='')
        show_ui()
        btn_close_video.place_forget()
        update_label("⛔ Real-time webcam detection stopped.")

    btn_close_video.config(command=close_webcam)
    btn_close_video.place(x=screen_width - 200, y=20)

    def process_frame():
        nonlocal alert_active, cooldown_counter
        if stop_video_flag or not cap.isOpened():
            cap.release()
            show_ui()
            video_label.config(image='')
            btn_close_video.place_forget()
            return

        ret, frame = cap.read()
        if not ret:
            return

        gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boxes, _ = hog.detectMultiScale(gray_full)
        person_count = len(boxes)

        resized = cv2.resize(frame, img_size)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        inp = np.expand_dims(gray, axis=(0, -1)).astype('float32') / 255.0

        prediction = model.predict(inp)[0][0]
        is_prediction_violent = prediction < confidence_threshold
        pred_queue.append(is_prediction_violent)

        violence_votes = sum(pred_queue)
        is_violent = (violence_votes >= 7) and (person_count >= 2)

        label = "Violence Detected" if is_violent else "No Event"
        color = (0, 0, 255) if is_violent else (0, 255, 0)

        if is_violent and not alert_active:
            cv2.imwrite("abc.png", frame)
            threading.Thread(target=mail, daemon=True).start()
            threading.Thread(target=play_alert, daemon=True).start()
            alert_active = True
            cooldown_counter = cooldown_frames

        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        cv2.putText(frame, f"People Detected: {person_count}", (5, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"Label: {label}", (5, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        display_frame = cv2.resize(frame, (screen_width, screen_height))
        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
        video_label.imgtk = img
        video_label.config(image=img)

        if alert_active:
            cooldown_counter -= 1
            if cooldown_counter <= 0:
                alert_active = False

        root.after(10, process_frame)

    process_frame()

# -- Video Upload & Detection Function --
def show_FDD_video(video_path):
    from tensorflow.keras.models import load_model
    global stop_video_flag
    stop_video_flag = False

    try:
        model = load_model('train_model.h5', compile=False)
    except Exception as e:
        update_label(f"Failed to load model: {e}")
        return

    cap = cv2.VideoCapture(video_path)
    frame_index = 1
    alert_active = False
    cooldown_counter = 0
    cooldown_frames = 7
    frame_skip = 2
    delay = 30
    img_size = (224, 224)
    violence_detected = False

    hide_ui()

    def close_video():
        global stop_video_flag
        stop_video_flag = True
        cap.release()
        video_label.config(image='')
        show_ui()
        btn_close_video.place_forget()
        update_label("⛔ Video manually stopped.")

    btn_close_video.config(command=close_video)
    btn_close_video.place(x=screen_width - 200, y=20)

    def process_frame():
        nonlocal frame_index, alert_active, cooldown_counter, violence_detected

        if stop_video_flag or not cap.isOpened():
            cap.release()
            show_ui()
            video_label.config(image='')
            btn_close_video.place_forget()
            msg = "✅ Video completed. ⚠️ Violence was detected." if violence_detected else "✅ Video completed. No violence detected."
            update_label(msg)
            return

        ret, frame = cap.read()
        if not ret:
            return

        if frame_index % frame_skip == 0:
            resized = cv2.resize(frame, img_size)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            inp = np.expand_dims(gray, axis=(0, -1)).astype('float32') / 255

            prediction = model.predict(inp)[0][0]
            is_violent = prediction < 0.5
            if is_violent:
                violence_detected = True

            label = "Violence Detected" if is_violent else "No Event"
            color = (0, 0, 255) if is_violent else (0, 255, 0)

            if is_violent and not alert_active:
                cv2.imwrite("abc.png", frame)
                threading.Thread(target=mail, daemon=True).start()
                threading.Thread(target=play_alert, daemon=True).start()
                alert_active = True
                cooldown_counter = cooldown_frames

            cv2.putText(frame, f"Frame: {frame_index}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"Label: {label}", (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            display_frame = cv2.resize(frame, (screen_width, screen_height))
            frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            video_label.imgtk = img
            video_label.config(image=img)

        if alert_active:
            cooldown_counter -= 1
            if cooldown_counter <= 0:
                alert_active = False

        frame_index += 1
        root.after(delay, process_frame)

    process_frame()

# -- Video File Selection --
def video_verify():
    file_path = askopenfilename(title="Select Video", filetypes=[("MP4 files", "*.mp4")])
    if file_path.lower().endswith('.mp4'):
        show_FDD_video(file_path)
    else:
        update_label("Invalid video file selected.")

# -- Run the GUI --
root.mainloop()
