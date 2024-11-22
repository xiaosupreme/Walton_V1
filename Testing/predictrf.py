import pandas as pd
import joblib

# Load the trained random forest model
model = joblib.load('occupancy_model.pkl')

# Prepare input data for prediction
data_to_predict = pd.DataFrame({
    'Year': [2024, 2024, 2024, 2024, 2024],
    'Month': [12, 12, 12, 12, 12],
    'Day': [31, 31, 31, 31, 31],
    'Room Type': ['Single', 'Double', 'Family', 'Suite', 'Deluxe']
})

# Encode Room Type (same mapping as during training)
room_type_mapping = {
    'Single': 0,
    'Double': 1,
    'Family': 2,
    'Suite': 3,
    'Deluxe': 4
}

# Apply the mapping to the Room Type column
data_to_predict['Room Type'] = data_to_predict['Room Type'].map(room_type_mapping)

# Check for any unmapped values
if data_to_predict['Room Type'].isnull().any():
    print("Warning: Some room types were not found in the mapping. Check your input.")

# Ensure the features are in the same order as when the model was trained
# The features for prediction must be in the order of ['Day', 'Month', 'Year', 'Room Type']
features = data_to_predict[['Day', 'Month', 'Year', 'Room Type']]

# Make predictions
predictions = model.predict(features)

# Print predictions
for i, room_type in enumerate(['Single', 'Double', 'Family', 'Suite', 'Deluxe']):
    print(f"Predicted occupancy for {room_type} on 2024-12-31: {predictions[i]:.2f}%")
