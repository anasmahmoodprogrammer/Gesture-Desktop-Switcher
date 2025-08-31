import cv2
import mediapipe as mp
import pyautogui
import time

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

prev_x = None
gesture_time = 0

def is_open_palm(landmarks):
    """Check if all fingers are extended (open palm)."""
    fingers = []
    fingers.append(landmarks[4].x > landmarks[3].x)  # Thumb (right hand assumption)
    fingers.append(landmarks[8].y < landmarks[6].y)   # Index
    fingers.append(landmarks[12].y < landmarks[10].y) # Middle
    fingers.append(landmarks[16].y < landmarks[14].y) # Ring
    fingers.append(landmarks[20].y < landmarks[18].y) # Pinky
    return all(fingers)

def is_fist(landmarks):
    """Check if all fingers are folded (fist)."""
    folded = []
    folded.append(landmarks[4].x < landmarks[3].x)   # Thumb
    folded.append(landmarks[8].y > landmarks[6].y)   # Index
    folded.append(landmarks[12].y > landmarks[10].y) # Middle
    folded.append(landmarks[16].y > landmarks[14].y) # Ring
    folded.append(landmarks[20].y > landmarks[18].y) # Pinky
    return all(folded)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("❌ Could not read from camera")
        break

    # Flip for mirror effect
    image = cv2.flip(image, 1)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Gesture detection
            x = hand_landmarks.landmark[9].x  # Palm center (index MCP)

            if prev_x is not None:
                dx = x - prev_x

                if time.time() - gesture_time > 1:
                    if dx > 0.15:  # Swipe Right
                        print("👉 Swipe Right → Next Desktop")
                        pyautogui.hotkey('ctrl', 'win', 'right')
                        gesture_time = time.time()

                    elif dx < -0.15:  # Swipe Left
                        print("👈 Swipe Left → Previous Desktop")
                        pyautogui.hotkey('ctrl', 'win', 'left')
                        gesture_time = time.time()

            # Open Palm → New Desktop
            if time.time() - gesture_time > 1 and is_open_palm(hand_landmarks.landmark):
                print("✋ Open Palm → New Desktop Created")
                pyautogui.hotkey('ctrl', 'win', 'd')
                gesture_time = time.time()

            # Fist → Close Desktop
            if time.time() - gesture_time > 1 and is_fist(hand_landmarks.landmark):
                print("✊ Fist → Close Current Desktop")
                pyautogui.hotkey('ctrl', 'win', 'f4')
                gesture_time = time.time()

            prev_x = x

    cv2.imshow("Gesture Desktop Manager", image)

    if cv2.waitKey(5) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
