import pandas as pd
import folium
from folium.plugins import HeatMap
import branca.colormap as cm  # Import for color legend

# Load your dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")  # Replace with your actual file

# Check if your data has the required columns
if 'Latitude' not in df.columns or 'Longitude' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Latitude', 'Longitude', and 'Total' columns.")

# Create a map centered around the mean location
map_center = [df["Latitude"].mean(), df["Longitude"].mean()]
heatmap = folium.Map(location=map_center, zoom_start=10)

# Convert Data to HeatMap format (latitude, longitude, target_column)
heat_data = df[['Latitude', 'Longitude', 'Total']].values.tolist()  

# Add HeatMap Layer with a smaller radius
HeatMap(heat_data, radius=10).add_to(heatmap)  # Adjust radius as needed

# **Add Color Legend (Sidebar)**
colormap = cm.LinearColormap(
    colors=['blue', 'green', 'yellow', 'orange', 'red'],  # Define color scale
    vmin=min(df['Total']),  # Minimum value
    vmax=max(df['Total']),  # Maximum value
    caption="Crash Frequency"  # Legend title
)
colormap.add_to(heatmap)  # Add to map

# Save as an HTML file
heatmap.save("truckCrashheatmap.html")

print("Heatmap with legend saved as heatmap.html")
