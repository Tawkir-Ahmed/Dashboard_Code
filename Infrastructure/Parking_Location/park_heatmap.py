import pandas as pd
import folium
from folium.plugins import HeatMap
import requests

# Define file path for truck parking locations
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_highway_data.csv"

# Load dataset
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    raise FileNotFoundError(f"File not found: {file_path}")

# Ensure required columns exist
required_columns = ['Latitude', 'Longitude', 'Name', 'Road Name', 'Nearest Highway', 'Distance to Highway (miles)']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Initialize a Folium map centered around Tennessee
m = folium.Map(location=[35.5175, -86.5804], zoom_start=7, tiles="cartodbpositron")

# Add Tennessee state boundaries using a GeoJSON file
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

# Add individual markers for truck parking locations with truck icons and popups
for index, row in df.iterrows():
    popup_text = f"""
    <b>Name:</b> {row.get('Name', 'Unknown')}<br>
    <b>Road:</b> {row.get('Road Name', 'Unknown')}<br>
    <b>Nearest Highway:</b> {row.get('Nearest Highway', 'Unknown')}<br>
    <b>Distance to Highway:</b> {row.get('Distance to Highway (miles)', 'N/A')} miles
    """
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="red", icon="truck", prefix="fa")  # Red marker with a truck icon
    ).add_to(m)

# Save map as HTML
output_file = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\truck_parking_heatmap.html"
m.save(output_file)

print(f"Truck parking heatmap with markers saved as '{output_file}'")
