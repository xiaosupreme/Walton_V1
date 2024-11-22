import os
import pickle
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


data_dict = pickle.load(open('./image_data.pickle', 'rb'))
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])


unique_labels, labels_encoded = np.unique(labels, return_inverse=True)


x_train, x_test, y_train, y_test = train_test_split(data, labels_encoded, test_size=0.2, random_state=42, stratify=labels_encoded)


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(len(data[0]),)),  
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(unique_labels), activation='softmax')  
])


model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])


history = model.fit(x_train, y_train, epochs=50, batch_size=32, validation_data=(x_test, y_test))


y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)


print("Classification Report:")
print(classification_report(y_test, y_pred_classes, target_names=unique_labels))


conf_matrix = confusion_matrix(y_test, y_pred_classes)
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


model.save('remote.h5')  
print("Model saved as 'remote.h5'")
 