import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

X = np.load("extracted/X.npy")
y = np.load("extracted/y.npy")

num_classes = len(np.unique(y))

print("Classes:", num_classes)


y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
    # stratify=y
)

model = Sequential([

    LSTM(
        128,
        return_sequences=True,
        input_shape=(30, 63)
    ),

    Dropout(0.2),

    LSTM(64),

    Dropout(0.2),

    Dense(64, activation='relu'),

    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

callback = EarlyStopping(
    patience=10,
    restore_best_weights=True
)

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=16,
    callbacks=[callback]
)

loss, acc = model.evaluate(X_test, y_test)

print("Accuracy:", acc)

model.save("models/bisindo_lstm.h5")

print("MODEL SAVED")