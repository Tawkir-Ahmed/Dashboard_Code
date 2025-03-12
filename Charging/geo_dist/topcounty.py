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

# Ensure 'County' column exists
if 'County' not in df.columns:
    raise ValueError("Missing required column: 'County'")

# Remove the word "County" from the 'County' column
df['County'] = df['County'].str.replace(" County", "", regex=False)

# Count occurrences of each County (after cleaning) and select the top 10
county_counts = df['County'].value_counts().reset_index().head(10)
county_counts.columns = ['County', 'Number of Charging Stations']

# Create an interactive bar chart using Plotly with different colors for each county
fig = px.bar(
    county_counts, 
    x='County', 
    y='Number of Charging Stations', 
    title="Top 10 Counties with EV Charging Stations in Tennessee",
    labels={'Number of Charging Stations': 'Count'},
    color='County',  # Assign different colors for each county
    text='Number of Charging Stations'  # Add frequency number on the bar
)

# Rotate x-axis labels for better visibility
fig.update_layout(xaxis_tickangle=-45)

# Improve the text visibility on bars
fig.update_traces(textposition='outside')

# Save as an HTML file
html_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Charging\geo_dist\charging_county_top10.html"
fig.write_html(html_file_path)

print(f"Interactive bar chart saved as '{html_file_path}'")
