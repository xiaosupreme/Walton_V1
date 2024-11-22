import os
import cv2
import mediapipe as mp


DATA_DIR = './image_data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 7  
dataset_size = 100      


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)


cap = cv2.VideoCapture(0)
for j in range(number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print(f'Collecting data for class {j}')

   
    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "Q" to start collecting! :)', (100, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            break

      
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        results = hands.process(img_rgb)

     
        if results.multi_hand_landmarks:
           
            hand_landmarks = results.multi_hand_landmarks[0]
            if hand_landmarks:  
               

              
                cv2.imwrite(os.path.join(DATA_DIR, str(j), f'{counter}.jpg'), frame)
                counter += 1

             
                cv2.putText(frame, f'Saved: {counter}/{dataset_size}', (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Hand not detected, try again.', (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, 'No hand landmarks detected.', (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

      
        cv2.imshow('frame', frame)
        cv2.waitKey(25)

cap.release()
cv2.destroyAllWindows()
