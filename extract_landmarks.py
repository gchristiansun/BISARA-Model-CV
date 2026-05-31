import os
import cv2
import numpy as np
import mediapipe as mp
from tqdm import tqdm

DATASET_PATH = "data/alfabet/training"
SEQUENCE_LENGTH = 30

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

classes = sorted(os.listdir(DATASET_PATH))

label_map = {
    label: idx
    for idx, label in enumerate(classes)
}

print(label_map)

X = []
y = []


def extract_landmarks(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    landmarks = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

    # FIX PENTING: selalu 126 dimensi
    if len(landmarks) == 63:
        landmarks.extend([0] * 63)

    if len(landmarks) == 0:
        landmarks = [0] * 126

    # FORCE SIZE
    if len(landmarks) < 126:
        landmarks.extend([0] * (126 - len(landmarks)))

    return landmarks[:126]


for label in classes:

    label_path = os.path.join(DATASET_PATH, label)

    videos = os.listdir(label_path)

    print(f"Processing {label}...")

    for video_name in tqdm(videos):

        video_path = os.path.join(label_path, video_name)

        cap = cv2.VideoCapture(video_path)

        frames = []

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            landmarks = extract_landmarks(frame)

            if len(landmarks) != 126:
                print("ERROR SHAPE:", len(landmarks))
                continue

            frames.append(landmarks)

        cap.release()

        if len(frames) == 0:
            continue

        # PAD / TRUNCATE
        if len(frames) < SEQUENCE_LENGTH:

            while len(frames) < SEQUENCE_LENGTH:
                frames.append([0] * 63)

        else:
            frames = frames[:SEQUENCE_LENGTH]

        X.append(frames)
        y.append(label_map[label])

X = np.array(X)
y = np.array(y)

print("X shape:", X.shape)
print("y shape:", y.shape)

os.makedirs("extracted", exist_ok=True)

np.save("extracted/X.npy", X)
np.save("extracted/y.npy", y)

print("DONE")