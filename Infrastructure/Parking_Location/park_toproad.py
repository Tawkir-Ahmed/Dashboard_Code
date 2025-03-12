# Re-import necessary libraries since the execution state was reset
import os
import pandas as pd
import plotly.express as px

# Define file path for truck parking locations
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_highway_data.csv"

# Check if file exists before loading
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load dataset
df = pd.read_csv(file_path)

# Ensure 'Road Name' column exists
if 'Road Name' not in df.columns:
    raise ValueError("Missing required column: 'Road Name'")

# Count occurrences of each Road Name and select the top 10
road_counts = df['Road Name'].value_counts().reset_index().head(10)
road_counts.columns = ['Road Name', 'Number of Truck Parking Locations']

# Create an interactive bar chart using Plotly with different colors for each road
fig = px.bar(
    road_counts, 
    x='Road Name', 
    y='Number of Truck Parking Locations', 
    title="Top 10 Roads with Truck Parking Locations in Tennessee",
    labels={'Number of Truck Parking Locations': 'Count'},
    color='Road Name',  # Assign different colors for each road
    text='Number of Truck Parking Locations'  # Add frequency number on the bar
)

# Rotate x-axis labels for better visibility
fig.update_layout(xaxis_tickangle=-45)

# Improve the text visibility on bars
fig.update_traces(textposition='outside')

# Save as an HTML file
html_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\top10_truck_parking_roads.html"
fig.write_html(html_file_path)

print(f"Interactive bar chart saved as '{html_file_path}'")
