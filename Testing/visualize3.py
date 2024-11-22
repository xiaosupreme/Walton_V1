import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from CSV
df = pd.read_csv('synthetic_data_cleaned2.csv')

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Add a new column for month
df['Month'] = df['Date'].dt.month  # Extract month as an integer

# Group by Month and Room Type, and calculate the average occupancy rate
average_monthly_occupancy = df.groupby(['Month', 'Room Type'])['Occupancy Rate (%)'].mean().unstack()

# Plotting
plt.figure(figsize=(12, 6))
average_monthly_occupancy.plot(marker='o', linestyle='-', ax=plt.gca())

# Customize the plot
plt.title('Average Monthly Occupancy Rates by Room Type (January to December)')
plt.xlabel('Month')
plt.ylabel('Average Occupancy Rate (%)')
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
plt.ylim(0, 100)

plt.grid()
plt.legend(title='Room Type')
plt.tight_layout()

for line in plt.gca().get_lines():
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        plt.text(x, y, f'{y:.1f}', ha='center', va='bottom', fontsize=8)
# Show the plot
plt.show()
