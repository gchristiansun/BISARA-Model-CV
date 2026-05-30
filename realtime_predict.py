import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model

SEQUENCE_LENGTH = 30

classes = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z'
]

model = load_model("models/bisindo_lstm.h5")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

sequence = deque(maxlen=SEQUENCE_LENGTH)

cap = cv2.VideoCapture(0)


def extract_landmarks(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        hand_landmarks = result.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        landmarks = []

        for lm in hand_landmarks.landmark:

            landmarks.extend([
                lm.x,
                lm.y,
                lm.z
            ])

        return landmarks

    return [0] * 63


while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    landmarks = extract_landmarks(frame)

    sequence.append(landmarks)

    if len(sequence) == SEQUENCE_LENGTH:

        input_data = np.expand_dims(sequence, axis=0)

        prediction = model.predict(input_data, verbose=0)

        class_id = np.argmax(prediction)

        confidence = prediction[0][class_id]

        label = classes[class_id]

        cv2.putText(
            frame,
            f"{label} ({confidence:.2f})",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("BISINDO Realtime", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()