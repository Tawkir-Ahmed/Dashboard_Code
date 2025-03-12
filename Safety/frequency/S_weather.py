import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Weather_Condition' not in df.columns or 'Crash_Type' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Weather_Condition', 'Crash_Type', and 'Total' columns.")

# Create a pivot table to calculate frequency from the 'Total' column
heatmap_data = df.pivot_table(values='Total', 
                              index='Weather_Condition', 
                              columns='Crash_Type', 
                              aggfunc='sum', 
                              fill_value=0)

# Create a heatmap using Plotly
fig = px.imshow(heatmap_data,
                labels={'x': 'Crash Type', 'y': 'Weather Condition', 'color': 'Crash Frequency'},
                title='Crash Type Frequency by Weather Condition')

# Rotate x-axis labels
fig.update_layout(
    xaxis=dict(
        title='Crash Type',
        tickangle=30  # Rotate x-axis labels by 45 degrees
    )
)

# Save the heatmap as an interactive HTML file
fig.write_html("Crash_Type_Weather_Condition_Heatmap.html")

print("Heatmap saved as Crash_Type_Weather_Condition_Heatmap.html")
