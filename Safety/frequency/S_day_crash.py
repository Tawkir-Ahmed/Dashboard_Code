import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Day' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Day' and 'Total' columns.")

# Aggregate crash frequency by day
day_crash_data = df.groupby("Day")["Total"].sum().reset_index()

# Create pie chart
fig = px.pie(
    day_crash_data, 
    names="Day", 
    values="Total", 
    title="Percentage Distribution of Crashes by Day",
    color_discrete_sequence=px.colors.sequential.Reds  # Adjust colors as needed
)

# Save as an interactive HTML file
fig.write_html("Truck_crash_distribution_by_day.html")

print("Pie chart saved as Truck_crash_distribution_by_day.html")
