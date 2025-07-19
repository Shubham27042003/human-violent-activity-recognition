import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque

# Load trained model
model = load_model('violence_detection_model.h5')

# Parameters
img_rows, img_cols = 64, 64
sequence_length = 20
frame_queue = deque(maxlen=sequence_length)

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized_frame = cv2.resize(frame, (img_rows, img_cols))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    frame_queue.append(gray_frame)

    if len(frame_queue) == sequence_length:
        input_frames = np.array(frame_queue).reshape(1, sequence_length, img_rows, img_cols, 1) / 255.0
        prediction = model.predict(input_frames)
        label = 'Violence' if np.argmax(prediction) == 1 else 'Non-Violence'
        color = (0, 0, 255) if label == 'Violence' else (0, 255, 0)
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('Real-Time Violence Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
