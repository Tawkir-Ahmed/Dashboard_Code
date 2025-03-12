import pandas as pd
import geopandas as gpd

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
gdf = gpd.read_file(tennessee_geojson_path)  # Load GeoJSON into a GeoDataFrame

# 📌 Ensure the column name for counties in GeoJSON is 'name'
gdf = gdf.rename(columns={"name": "County"})
gdf["County"] = gdf["County"].str.title()  # Ensure consistent formatting

# 📌 Merge the factory data with GeoJSON data
df_county = df['County'].value_counts().reset_index()
df_county.columns = ['County', 'BusinessCount']
df_county["County"] = df_county["County"].str.title()  # Ensure matching case

# 📌 Calculate the frequency of counties in the GeoJSON
geojson_county = gdf['County'].value_counts().reset_index()
geojson_county.columns = ['County', 'GeoJSONCount']

# 📌 Merge both frequencies into one dataframe for comparison
county_comparison = pd.merge(df_county, geojson_county, on='County', how='left')
county_comparison['GeoJSONCount'] = county_comparison['GeoJSONCount'].fillna(0)  # Fill NaN values with 0 for missing counties

# 📌 Find counties in the data that are not in the GeoJSON
missing_counties = county_comparison[county_comparison['GeoJSONCount'] == 0]

# 📌 Save the comparison table as an HTML file
output_html_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\county_comparison_factory.html"
county_comparison.to_html(output_html_path, index=False)

# 📌 Optionally, print the comparison in the console
print("County Comparison Table:")
print(county_comparison)

# 📌 Inform user about the output file
print(f"✅ County comparison table saved as HTML at: {output_html_path}")
