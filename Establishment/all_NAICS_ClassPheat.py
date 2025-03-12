import os
import folium
import pandas as pd
from folium.plugins import HeatMap

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

# 📌 Initialize a Folium map centered on Tennessee
m = folium.Map(
    location=[35.5175, -86.5804],  # Tennessee's center
    tiles="Cartodb Positron",
    zoom_start=7,
    width="100%",
    height="100%"
)

# 📌 Add a heatmap based on the Latitude and Longitude from the dataset
heat_data = df[['Latitude', 'Longitude']].values  # Extract Latitude and Longitude
heatmap = HeatMap(heat_data, radius=15, blur=10, max_zoom=13)
m.add_child(heatmap)

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

# 📌 JavaScript to filter heatmap points dynamically based on selected class
js = """
    <script>
        function filterMap() {
            var selectedClass = document.getElementById('classDropdown').value;
            var filteredData = [];  // Initialize empty array to hold filtered points
            
            {% for row in df.iterrows() %}
                var lat = "{{ row[1]['Latitude'] }}";
                var lon = "{{ row[1]['Longitude'] }}";
                var className = "{{ row[1]['Class'] }}";
                
                // If class matches selected class, add point to filteredData
                if (selectedClass === "" || className === selectedClass) {
                    filteredData.push([lat, lon]);
                }
            {% endfor %}
            
            // Re-create the heatmap layer with filtered data
            var heatmapLayer = new HeatMapLayer({data: filteredData, radius: 15, blur: 10, maxZoom: 13});
            map.addLayer(heatmapLayer);  // Add new heatmap layer to the map
        }
    </script>
"""

# Add the dropdown and JavaScript to the map
m.get_root().html.add_child(folium.Element(dropdown))
m.get_root().html.add_child(folium.Element(js))

# 📌 Add dark mode toggle
folium.TileLayer("cartodbdark_matter", name="Dark Mode", control=True).add_to(m)
folium.TileLayer("cartodbpositron", name="Light Mode", control=True).add_to(m)

# 📌 Save the map
save_folder = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "NAICS_heatmap_with_class_filter2.html")
m.save(save_path)

print(f"✅ Heatmap with dynamic class filtering saved at: {save_path}")
