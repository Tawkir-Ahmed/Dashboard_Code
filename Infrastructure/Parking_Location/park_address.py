# Re-import necessary libraries
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

# Ensure the 'Rating' and 'Address' columns exist
if 'Rating' not in df.columns or 'Address' not in df.columns:
    raise ValueError("Missing required columns: 'Rating' or 'Address'")

# Convert 'Rating' column to numeric (handle errors in case of non-numeric values)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Select the top 10 parking stations based on the actual rating (no averaging)
popular_parking = df[['Address', 'Rating']].dropna().sort_values(by='Rating', ascending=False).head(10)

# Create an interactive bar chart for popular parking stations
fig = px.bar(
    popular_parking, 
    x='Address', 
    y='Rating', 
    title="Top 10 Popular Truck Parking Stations in Tennessee",
    labels={'Rating': 'Rating'},
    color='Rating',  # Assign different colors based on rating
    text='Rating'  # Display rating values on bars
)

# Rotate x-axis labels for better visibility
fig.update_layout(xaxis_tickangle=-45)

# Improve text visibility on bars
fig.update_traces(textposition='outside')

# Save as an HTML file
html_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\top10_popular_parking.html"
fig.write_html(html_file_path)

print(f"Interactive bar chart of popular parking stations saved as '{html_file_path}'")
