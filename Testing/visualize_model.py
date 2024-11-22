import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load the trained random forest model
model = joblib.load('occupancy_model.pkl')

# Define room types
room_types = ['Single', 'Double', 'Family', 'Suite', 'Deluxe']

# Create a date range for the year 2025
date_range = pd.date_range(start='2025-01-01', end='2025-12-31')

# Prepare an empty list to hold the predictions
predictions = []

# Mapping for Room Type encoding
room_type_mapping = {
    'Single': 0,
    'Double': 1,
    'Family': 2,
    'Suite': 3,
    'Deluxe': 4
}

# Generate predictions for each room type for each day
for single_date in date_range:
    for room_type in room_types:
        # Prepare input data for the model
        input_data = pd.DataFrame({
            'Year': [single_date.year],
            'Month': [single_date.month],
            'Day': [single_date.day],
            'Room Type': [room_type]
        })

        # Map the Room Type to numerical values
        input_data['Room Type'] = input_data['Room Type'].map(room_type_mapping)

        # Ensure the features are in the same order as when the model was trained
        features = input_data[['Day', 'Month', 'Year', 'Room Type']]

        # Make prediction
        predicted_occupancy = model.predict(features)

        # Append the results to the predictions list
        predictions.append({
            'Date': single_date,
            'Room Type': room_type,
            'Predicted Occupancy Rate (%)': predicted_occupancy[0]
        })

# Create a DataFrame from the predictions list
predictions_df = pd.DataFrame(predictions)

# Plotting the results
plt.figure(figsize=(14, 8))
for room_type in room_types:
    room_data = predictions_df[predictions_df['Room Type'] == room_type]
    plt.plot(room_data['Date'], room_data['Predicted Occupancy Rate (%)'], label=room_type)

plt.title('Predicted Occupancy Rates for Each Room Type in 2025')
plt.xlabel('Date')
plt.ylabel('Predicted Occupancy Rate (%)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()
