import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the data
with open("hotel_chatbot_intent_data.json", "r") as f:
    data = json.load(f)

# Separate text and labels
texts = [entry['text'] for entry in data]
labels = [entry['intent'] for entry in data]

# Split data into training and testing sets
texts_train, texts_test, labels_train, labels_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Step 1: Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed
X_train = vectorizer.fit_transform(texts_train)
X_test = vectorizer.transform(texts_test)

# Step 2: Train a Logistic Regression model
model = LogisticRegression(max_iter=200)  # Increase max_iter if the model doesn't converge
model.fit(X_train, labels_train)

# Step 3: Evaluate the model (optional, but recommended for tuning)
predictions = model.predict(X_test)
accuracy = accuracy_score(labels_test, predictions)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Step 4: Save the trained model and vectorizer to files
joblib.dump(model, "intent_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model and vectorizer saved successfully!")
