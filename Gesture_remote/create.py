import os
import pickle
import mediapipe as mp
import cv2


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './image_data'

def process_image(img_path):
    """Processes a single image to extract hand landmarks."""
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error reading image: {img_path}")
        return None, None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
      
        hand_landmarks = results.multi_hand_landmarks[0]
        x_coords = [lm.x for lm in hand_landmarks.landmark]
        y_coords = [lm.y for lm in hand_landmarks.landmark]
        
        normalized_data = [(x - min(x_coords)) for x in x_coords] + \
                          [(y - min(y_coords)) for y in y_coords]
        return normalized_data, True

    return None, False

def collect_data(data_dir):
    """Collects hand landmarks data from images in the specified directory."""
    data = []
    labels = []
    
    for dir_ in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, dir_)
        if not os.path.isdir(class_dir):
            continue
        
        for img_path in os.listdir(class_dir):
            img_full_path = os.path.join(class_dir, img_path)
            landmarks, valid = process_image(img_full_path)
            if valid:
                data.append(landmarks)
                labels.append(dir_)

    return data, labels


data, labels = collect_data(DATA_DIR)


with open('image_data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)
print("Data saved as image_data.pickle'")
print(f"Collected {len(data)} samples with {len(set(labels))} unique labels.")
