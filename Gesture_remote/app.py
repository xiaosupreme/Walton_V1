import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import mediapipe as mp
import pyautogui
import time


model = load_model('remote.h5')


gesture_labels = {
    0: 'Detect Space',
    1: 'Detect Left',
    2: 'Detect Right',
    3: 'Detect Up',
    4: 'Detect Down',
    5: 'Detect V Down',
    6: 'Detect V Up'
}


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  


current_gesture = None
space_triggered = False
video_output = True
running = True  
last_trigger_time = 0  

def trigger_key_action(gesture):
    """Trigger keyboard actions based on detected gesture."""
    global space_triggered, last_trigger_time

    current_time = time.time()

   
    if gesture == 0 and not space_triggered:
        pyautogui.press('space')
        print("Triggered space")
        space_triggered = True  

   
    elif gesture in [1, 2, 3, 4, 5, 6] and (current_time - last_trigger_time >= 0.5):
        if gesture == 1:  
            pyautogui.press('left')
            print("Triggered Left")
        elif gesture == 2:  
            pyautogui.press('right')
            print("Triggered Right")
        elif gesture == 3:  
            pyautogui.press('up')
            print("Triggered Up")
        elif gesture == 4:  
            pyautogui.press('down')
            print("Triggered Down")
        elif gesture == 5: 
            pyautogui.press('volumedown')
            print("Triggered V Down")
        elif gesture == 6:  
            pyautogui.press('volumeup')
            print("Triggered V Up")

       
        last_trigger_time = current_time

def extract_landmarks(frame):
    """Extract hand landmarks from the camera frame."""
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        x_coords = [lm.x for lm in hand_landmarks.landmark]
        y_coords = [lm.y for lm in hand_landmarks.landmark]
        normalized_data = [(x - min(x_coords)) for x in x_coords] + \
                          [(y - min(y_coords)) for y in y_coords]
        return normalized_data, hand_landmarks
    return None, None

def reset_controls():
    """Reset all control flags when no hand is detected."""
    global current_gesture, space_triggered
    current_gesture = None
    space_triggered = False
    print("Stopped all controls")


confidence_threshold = 0.85

while running:
   
    ret, frame = cap.read()
    if not ret:
        break

   
    landmarks, hand_landmarks = extract_landmarks(frame)

    if landmarks is not None:
        landmarks = np.expand_dims(landmarks, axis=0)

       
        predictions = model.predict(landmarks)
        predicted_class = np.argmax(predictions[0])
        predicted_confidence = predictions[0][predicted_class]

        if predicted_confidence > confidence_threshold:
            gesture_text = f"{gesture_labels[predicted_class]} ({predicted_confidence:.2f})"
            trigger_key_action(predicted_class)

            if video_output:
             
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
                control_text = f"Control: {gesture_labels[predicted_class]}"
                cv2.putText(frame, control_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            reset_controls()  

    else:
        reset_controls() 

  
    if video_output:
        cv2.imshow('Gesture Detection', frame)

   
    key = cv2.waitKey(1) & 0xFF
    if key in [27, ord('q')]:  
        running = False
    elif key == ord('v'):  
        video_output = not video_output
        print(f"Video Output: {'On' if video_output else 'Off'}")


cap.release()
cv2.destroyAllWindows()
