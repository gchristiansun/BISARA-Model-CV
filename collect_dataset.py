import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import os

SEQUENCE_LENGTH = 30

classes = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z'
]

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

X = []
y = []

sequence = deque(maxlen=SEQUENCE_LENGTH)

current_label = None
recording = False


def extract_landmarks(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    landmarks = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

    if len(landmarks) == 63:
        landmarks.extend([0] * 63)

    if len(landmarks) == 0:
        landmarks = [0] * 126

    return landmarks[:126]


cap = cv2.VideoCapture(0)

print("Controls:")
print("Press A-Z to select label")
print("Press SPACE to start/stop recording")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    landmarks = extract_landmarks(frame)

    if recording and current_label is not None:
        sequence.append(landmarks)

        cv2.putText(frame, "RECORDING...", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        if len(sequence) == SEQUENCE_LENGTH:
            X.append(list(sequence))
            y.append(classes.index(current_label))
            sequence.clear()
            print(f"Saved sample for {current_label}")

    cv2.putText(frame, f"Label: {current_label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Dataset Collector", frame)

    key = cv2.waitKey(1) & 0xFF

    # select label
    if 65 <= key <= 90:  # A-Z
        current_label = chr(key)
        print("Selected:", current_label)

    # toggle recording
    if key == 32:  # SPACE
        recording = not recording
        sequence.clear()
        print("Recording:", recording)

    # quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# SAVE DATASET
X = np.array(X, dtype=np.float32)
y = np.array(y)

os.makedirs("dataset", exist_ok=True)

np.save("dataset/X.npy", X)
np.save("dataset/y.npy", y)

print("DONE SAVING DATASET")
print("X shape:", X.shape)
print("y shape:", y.shape)