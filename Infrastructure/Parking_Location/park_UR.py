import os
import pandas as pd
import plotly.express as px

# Define file path for truck parking locations
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_highway_data.csv"

# Load dataset
df = pd.read_csv(file_path)

# Ensure the 'City' column exists
if 'City' not in df.columns:
    raise ValueError("Missing required column: 'City'")

# Classify locations as Urban (City) or Rural (N/A)
df['Location Type'] = df['City'].apply(lambda x: 'Rural' if pd.isna(x) or x == 'N/A' else 'Urban')

# Count occurrences of each category
location_counts = df['Location Type'].value_counts()

# Define light colors for better visibility
color_map = {'Urban': '#a3c1ad', 'Rural': '#f4c2c2'}  # Light green and light red

# Create the pie chart with larger percentage text
fig = px.pie(
    names=location_counts.index,
    values=location_counts.values,
    title="Distribution of Truck Parking Locations: Urban vs Rural",
    color=location_counts.index,
    color_discrete_map=color_map,
    hole=0.3  # Optional: Adds a donut-like effect
)

# Increase percentage text size
fig.update_traces(
    textinfo='percent+label',  # Show both percentage and label
    textfont_size=20  # Increase text size
)

# Save as an HTML file
html_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\UR_pie_plot.html"
fig.write_html(html_file_path)

print(f"Pie chart with increased percentage text saved as '{html_file_path}'")
