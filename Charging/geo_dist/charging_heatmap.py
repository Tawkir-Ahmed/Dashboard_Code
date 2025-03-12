import pandas as pd
import folium
from folium.plugins import HeatMap
import requests

# Load your dataset
file_path = r"D:\Mobility Report & Dashboard\EV_Charging_data\charge_county_zip_city.csv"  # Update with your file path
df = pd.read_csv(file_path)

# Ensure required columns exist
required_columns = ['Latitude', 'Longitude', 'Name', 'Address', 'County']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Initialize a Folium map centered around Tennessee
m = folium.Map(location=[35.5175, -86.5804], zoom_start=7, tiles="cartodbpositron")  # Light tile layer

# Add Tennessee state boundaries using a dedicated Tennessee GeoJSON file
tennessee_geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/tennessee.geojson"
try:
    response = requests.get(tennessee_geojson_url)
    geojson_data = response.json()
    folium.GeoJson(
        geojson_data,
        name="Tennessee Borders",
        style_function=lambda x: {"fillColor": "transparent", "color": "black", "weight": 2},
    ).add_to(m)
except Exception as e:
    print(f"Error loading Tennessee GeoJSON: {e}")

# Convert DataFrame to a list of coordinate pairs for the HeatMap
heat_data = df[['Latitude', 'Longitude']].dropna().values.tolist()

# Add heatmap layer with customization
HeatMap(heat_data, radius=12, blur=15, min_opacity=0.3).add_to(m)

# Add individual markers for EV charging stations with formatted popups
for index, row in df.iterrows():
    popup_text = f"""
    Name: {row.get('Name', 'Unknown')}
    Address: {row.get('Address', 'Unknown')}
    County: {row.get('County', 'Unknown')}
    """
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="blue", icon="bolt", prefix="fa")  # Blue marker with EV bolt icon
    ).add_to(m)

# Save map as HTML
output_file = r"D:\Mobility Report & Dashboard\Dashboard_Code\Charging\ev_charging_heatmap.html"  # Update path if needed
m.save(output_file)

print(f"Heatmap with Tennessee boundaries saved as '{output_file}'")
