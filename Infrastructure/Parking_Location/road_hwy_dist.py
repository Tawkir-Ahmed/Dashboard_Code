# Re-import necessary libraries
import os
import pandas as pd

# Define file path for truck parking locations
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_highway_data.csv"

# Check if file exists before loading
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load dataset
df = pd.read_csv(file_path)

# Ensure required columns exist before proceeding
required_columns = ['Address', 'County', 'Road Name', 'Distance to Highway (miles)']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: '{col}'")

# Sort the truck parking table by "Distance to Highway (miles)" in ascending order
truck_parking_table_sorted = df[['Address', 'County', 'Road Name', 'Distance to Highway (miles)']].dropna().sort_values(by='Distance to Highway (miles)')

# Define the output HTML file path
html_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\sorted_truck_parking.html"

# Save the sorted table as an HTML file
truck_parking_table_sorted.to_html(html_file_path, index=False)

print(f"Sorted truck parking table saved as '{html_file_path}'")

