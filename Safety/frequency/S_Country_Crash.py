import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'County' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'County' and 'Total' columns.")

# Aggregate crash frequency by county and sort in descending order
county_crash_data = df.groupby("County")["Total"].sum().reset_index()
county_crash_data = county_crash_data.sort_values(by="Total", ascending=False)  # Sort from highest to lowest

# Create bar chart
fig = px.bar(
    county_crash_data, 
    x="County", 
    y="Total", 
    title="Total Crash Frequency by County",
    labels={"Total": "Total Crashes", "County": "County"},
    color="Total",
    color_continuous_scale="reds"
)

# Customize layout
fig.update_layout(xaxis_tickangle=-45)

# Save as an interactive HTML file
fig.write_html("Truck_county_crash_frequency.html")

print("Bar chart saved as Truck_county_crash_frequency.html")
