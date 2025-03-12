import os
import folium
import pandas as pd
import geopandas as gpd
import requests
from folium.plugins import StripePattern

# 📌 Load factory data
data_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\all_factories_zip.csv"
df = pd.read_csv(data_path)

# 📌 Ensure required columns exist
required_columns = ['Latitude', 'Longitude', 'County']
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
    folium.Choropleth(
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

    # 📌 Add interactive hover tooltips
    style_function = lambda x: {"fillColor": "#ffffff", "color": "#000000", "fillOpacity": 0.1, "weight": 0.1}
    highlight_function = lambda x: {"fillColor": "#000000", "color": "#000000", "fillOpacity": 0.50, "weight": 0.1}

    NIL = folium.features.GeoJson(
        data=merged_gdf,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["County", "FactoryCount"],
            aliases=["County:", "Factory Count:"],
            style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
        )
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)

    # 📌 Add cross-hatching for missing values
    missing_counties = df_county[df_county["FactoryCount"] == 0]["County"].values
    missing_gdf = df_county[df_county["County"].isin(missing_counties)]

    sp = StripePattern(angle=45, color="grey", space_color="white")
    sp.add_to(m)
    folium.features.GeoJson(
        name="No Factory Data",
        data=missing_gdf,
        style_function=lambda x: {"fillPattern": sp},
        show=True
    ).add_to(m)

else:
    print("⚠️ Choropleth skipped due to missing GeoJSON data.")

# 📌 Add dark mode toggle
folium.TileLayer("cartodbdark_matter", name="Dark Mode", control=True).add_to(m)
folium.TileLayer("cartodbpositron", name="Light Mode", control=True).add_to(m)

# 📌 Add layer controller
folium.LayerControl(collapsed=False).add_to(m)

# 📌 Save the map
save_folder = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "factory_choropleth.html")
m.save(save_path)

print(f"✅ Choropleth map saved at: {save_path}")
