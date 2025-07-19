import numpy as np
import os
import cv2
import gc
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Conv2D, MaxPooling2D, Flatten, Dense,
                                     Dropout, BatchNormalization)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Settings
img_height, img_width = 224, 224
input_shape = (img_height, img_width, 3)
class_1_path = r"E:/final year project/train/data/1"
class_0_path = r"E:/final year project/train/data/0"

def load_data():
    data = []
    labels = []

    for label, folder in enumerate([class_1_path, class_0_path]):
        for file in os.listdir(folder):
            try:
                img_path = os.path.join(folder, file)
                img = cv2.imread(img_path)
                img = cv2.resize(img, (img_width, img_height))
                data.append(img)
                labels.append(label)
            except Exception as e:
                print(f"Failed loading {img_path}: {e}")

    data = np.array(data, dtype='float32') / 255.0
    labels = to_categorical(labels, 2)
    return data, labels

def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.0003),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def main():
    print("📥 Loading data...")
    X, y = load_data()
    X, y = shuffle(X, y, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True
    )
    datagen.fit(X_train)

    print(f"Training: {X_train.shape[0]}, Testing: {X_test.shape[0]}")

    model = build_model()
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
        ModelCheckpoint("train_model.h5", save_best_only=True, monitor='val_loss')
    ]

    model.fit(datagen.flow(X_train, y_train, batch_size=32),
              validation_data=(X_test, y_test),
              epochs=20,
              callbacks=callbacks)

    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"✅ Accuracy: {test_acc*100:.2f}%")

if __name__ == "__main__":
    main()
