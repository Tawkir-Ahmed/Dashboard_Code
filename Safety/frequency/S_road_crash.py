import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Roadway_Name' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Roadway_Name' and 'Total' columns.")

# Group by 'Roadway_Name' and sum 'Total' crashes for each roadway
roadway_crash_data = df.groupby('Roadway_Name').agg({'Total': 'sum'}).reset_index()

# Sort the data from highest to lowest based on the 'Total' crashes
roadway_crash_data = roadway_crash_data.sort_values(by='Total', ascending=False)

# Select the top 15 roadways with the highest total crashes
top_15_roadways = roadway_crash_data.head(20)

# Create bar plot for total crashes by Roadway_Name
fig = px.bar(
    top_15_roadways,
    x="Roadway_Name",  # Roadway names on the x-axis
    y="Total",  # Total crashes on the y-axis
    title="Top 15 Truck Crashes by Roadway Name",
    labels={"Total": "Crash Frequency", "Roadway_Name": "Roadway Name"},
    color="Roadway_Name",  # Optional: Color bars by Roadway_Name
    text="Total"  # Optional: Show total crash values on the bars
)

# Show the plot
fig.show()

# Save the plot as an interactive HTML file
fig.write_html("Top_15_Total_crashes_by_Roadway_Name_barplot.html")

print("Bar plot saved as Top_15_Total_crashes_by_Roadway_Name_barplot.html")
