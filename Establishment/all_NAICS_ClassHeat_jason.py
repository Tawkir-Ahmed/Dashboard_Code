import os
import folium
import pandas as pd
import geopandas as gpd
from folium.plugins import StripePattern

# 📌 Load factory data
data_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated.csv"
df = pd.read_csv(data_path)

# 📌 Ensure required columns exist
required_columns = ['Latitude', 'Longitude', 'County', 'Class']  # Include Class in required columns
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# 📌 Drop rows with missing County data
df.dropna(subset=['County'], inplace=True)

# 📌 Remove the 'County' suffix from the 'County' column in your data to match GeoJSON
df['County'] = df['County'].str.replace(r' County$', '', regex=True)

# 📌 Load Tennessee counties GeoJSON (Ensure this file exists)
tennessee_geojson_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\tennesseeboundaries.geojson"

try:
    gdf = gpd.read_file(tennessee_geojson_path)  # Load GeoJSON into a GeoDataFrame
    print("✅ Tennessee County GeoJSON loaded successfully.")
except Exception as e:
    print(f"⚠️ Error loading Tennessee County GeoJSON: {e}")
    gdf = None

# 📌 Merge county factory counts with GeoJSON
df_county = df.groupby("County").size().reset_index(name="FactoryCount")
df_county["County"] = df_county["County"].str.title()  # Ensure county names match

# 📌 Check the column name for county names in the GeoJSON file and ensure it's 'name'
if gdf is not None:
    gdf = gdf.rename(columns={"name": "County"})  # Ensure the column is named 'County' to match the data frame
    gdf["County"] = gdf["County"].str.title()  # Ensure consistent formatting
    merged_gdf = gdf.merge(df_county, on="County", how="left").fillna(0)  # Merge factory data
else:
    merged_gdf = None

# 📌 Initialize a Folium map centered on Tennessee
m = folium.Map(
    location=[35.5175, -86.5804],  # Tennessee's center
    tiles="Cartodb Positron",
    zoom_start=7,
    width="100%",
    height="100%"
)

# 📌 Add Choropleth map (Only if GeoJSON data is valid)
if merged_gdf is not None:
    choropleth = folium.Choropleth(
        geo_data=merged_gdf,
        name="Factory Density",
        data=df_county,
        columns=["County", "FactoryCount"],
        key_on="feature.properties.County",  # Adjust this to match the county names in GeoJSON
        fill_color="YlGnBu",
        fill_opacity=1,  # Set opacity to 50%
        line_opacity=0.2,
        legend_name="Factory Count by County",
        nan_fill_color="white"
    ).add_to(m)

else:
    print("⚠️ Choropleth skipped due to missing GeoJSON data.")

# 📌 Add dark mode toggle
folium.TileLayer("cartodbdark_matter", name="Dark Mode", control=True).add_to(m)
folium.TileLayer("cartodbpositron", name="Light Mode", control=True).add_to(m)

# 📌 Create a dropdown to filter the map by class
dropdown = """
    <select id="classDropdown" onchange="filterMap()">
        <option value="">Select Class</option>
        <option value="Retail and Consumer Goods">Retail and Consumer Goods</option>
        <option value="Services">Services</option>
        <option value="Manufacturing and Industrial">Manufacturing and Industrial</option>
        <option value="Transportation and Warehousing">Transportation and Warehousing</option>
        <option value="Agriculture and Farming">Agriculture and Farming</option>
        <option value="Healthcare and Social Services">Healthcare and Social Services</option>
        <option value="Real Estate and Property">Real Estate and Property</option>
        <option value="Government and Non-Profit">Government and Non-Profit</option>
        <option value="Technology and IT">Technology and IT</option>
        <option value="Entertainment and Recreation">Entertainment and Recreation</option>
        <option value="Wholesale and Distribution">Wholesale and Distribution</option>
        <option value="Construction and Building">Construction and Building</option>
        <option value="Utilities">Utilities</option>
    </select>
"""

# 📌 JavaScript to update choropleth colors and scale dynamically based on selected class
js = """
    <script>
        function filterMap() {
            var selectedClass = document.getElementById('classDropdown').value;
            var choroplethLayer = document.querySelector(".leaflet-interactive");

            choroplethLayer.setStyle({
                fillColor: function(feature) {
                    if (selectedClass === "" || feature.properties.Class === selectedClass) {
                        return 'green';
                    } else {
                        return 'white';
                    }
                }
            });

            // Update the scale according to the class
            var scale = document.querySelector(".leaflet-control-legend");
            if (scale) {
                scale.innerHTML = 'Factory Count by Class: ' + selectedClass;
            }
        }
    </script>
"""

# Add the dropdown and JS to the map
m.get_root().html.add_child(folium.Element(dropdown))
m.get_root().html.add_child(folium.Element(js))

# 📌 Save the map
save_folder = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "NAICS_choropleth_with_dynamic_class_filter.html")
m.save(save_path)

print(f"✅ Choropleth map with dynamic class filtering saved at: {save_path}")
