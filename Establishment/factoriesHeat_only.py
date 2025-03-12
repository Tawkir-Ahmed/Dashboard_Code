import os
import folium
import pandas as pd
from folium.plugins import HeatMap

# 📌 Load factory data
data_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\factories1_zip.csv"
df = pd.read_csv(data_path)

# 📌 Ensure required columns exist
required_columns = ['Latitude', 'Longitude', 'County']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# 📌 Drop rows with missing County data
df.dropna(subset=['County'], inplace=True)

# 📌 Initialize a Folium map centered on Tennessee
m = folium.Map(
    location=[35.5175, -86.5804],  # Tennessee's center
    tiles="Cartodb Positron",
    zoom_start=7,
    width="100%",
    height="100%"
)

# 📌 Add Heatmap
# Prepare the data for the heatmap (Latitude, Longitude)
heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]

HeatMap(heat_data).add_to(m)

# 📌 Add dark mode toggle
folium.TileLayer("cartodbdark_matter", name="Dark Mode", control=True).add_to(m)
folium.TileLayer("cartodbpositron", name="Light Mode", control=True).add_to(m)

# 📌 Add layer controller
folium.LayerControl(collapsed=False).add_to(m)

# 📌 Save the map
save_folder = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "factory_heatmap.html")
m.save(save_path)

print(f"✅ Heatmap saved at: {save_path}")
