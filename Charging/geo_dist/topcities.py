import pandas as pd
import plotly.express as px
import os

# Corrected File Path
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Charging\charge_county_zip_city.csv"

# Check if file exists before loading
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load dataset
df = pd.read_csv(file_path)

# Ensure 'City' column exists
if 'City' not in df.columns:
    raise ValueError("Missing required column: 'City'")

# Count occurrences of each City and select the top 10
city_counts = df['City'].value_counts().reset_index().head(10)
city_counts.columns = ['City', 'Number of Charging Stations']

# Create an interactive bar chart using Plotly with different colors for each city
fig = px.bar(
    city_counts, 
    x='City', 
    y='Number of Charging Stations', 
    title="Top 10 Cities with EV Charging Stations in Tennessee",
    labels={'Number of Charging Stations': 'Count'},
    color='City',  # Assign different colors for each city
    text='Number of Charging Stations'  # Add frequency number on the bar
)

# Rotate x-axis labels for better visibility
fig.update_layout(xaxis_tickangle=-45)

# Improve the text visibility on bars
fig.update_traces(textposition='outside')

# Save as an HTML file
html_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Charging\geo_dist\charging_city_top10.html"
fig.write_html(html_file_path)

print(f"Interactive bar chart saved as '{html_file_path}'")
