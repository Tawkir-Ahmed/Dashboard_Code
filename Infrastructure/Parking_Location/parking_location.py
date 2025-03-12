"""
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the cleaned file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_truck_filtered.csv"
df = pd.read_csv(file_path)

# Check if Latitude and Longitude columns exist
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    raise ValueError("Latitude and Longitude columns are required in the dataset.")

# Initialize Geolocator with Nominatim
geolocator = Nominatim(user_agent="parking_locator")

# Rate limiter to avoid request overload
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1, max_retries=3, error_wait_seconds=2.0)

# Function to get County, ZIP Code, City Name, and Highway/Interstate from Latitude and Longitude
def get_location_info(lat, lon):
    try:
        location = geocode((lat, lon), language='en')
        if location:
            address = location.raw.get('address', {})
            state = address.get('state', 'N/A')

            # Only include if State is Tennessee
            if state == 'Tennessee':
                county = address.get('county', 'N/A')
                zip_code = address.get('postcode', 'N/A')
                city = address.get('city', address.get('town', address.get('village', 'N/A')))
                
                # Identify if the location is on a highway or interstate
                road_name = address.get('road', 'N/A')
                if any(keyword in road_name for keyword in ["Interstate", "I-", "Highway", "US Route"]):
                    highway = road_name
                else:
                    highway = "Not on Interstate/Highway"

                return county, zip_code, city, highway
            else:
                print(f"Skipping non-Tennessee location: {state}")
                return 'Out of Tennessee', 'N/A', 'N/A', 'N/A'
    except Exception as e:
        print(f"Error: {e}")
    return 'N/A', 'N/A', 'N/A', 'N/A'

# Apply function to each row and add new columns
df['County'], df['ZIP Code'], df['City'], df['Highway/Interstate'] = zip(*df.apply(lambda row: get_location_info(row['Latitude'], row['Longitude']), axis=1))

# Filter out rows that are not in Tennessee
df = df[df['County'] != 'Out of Tennessee']

# Save the updated DataFrame
updated_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_county_zip_city_highway.csv"
df.to_csv(updated_file_path, index=False)

print(f"Updated file saved with County, ZIP Code, City Name, and Highway/Interstate as '{updated_file_path}'")
"""


import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
import requests
import time

# Load the cleaned file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_truck_filtered.csv"
df = pd.read_csv(file_path)

# Check if Latitude and Longitude columns exist
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    raise ValueError("Latitude and Longitude columns are required in the dataset.")

# Initialize Geolocator with Nominatim
geolocator = Nominatim(user_agent="parking_locator")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1, max_retries=3, error_wait_seconds=2.0)

# Function to get road name and county, ZIP Code, City Name
def get_location_info(lat, lon):
    try:
        location = geocode((lat, lon), language='en')
        if location:
            address = location.raw.get('address', {})
            state = address.get('state', 'N/A')

            # Only process locations in Tennessee
            if state == 'Tennessee':
                county = address.get('county', 'N/A')
                zip_code = address.get('postcode', 'N/A')
                city = address.get('city', address.get('town', address.get('village', 'N/A')))
                road_name = address.get('road', 'Unknown Road')  # Extract Road Name

                return county, zip_code, city, road_name
            else:
                print(f"Skipping non-Tennessee location: {state}")
                return 'Out of Tennessee', 'N/A', 'N/A', 'N/A'
    except Exception as e:
        print(f"Error: {e}")
    return 'N/A', 'N/A', 'N/A', 'N/A'

# Function to find the nearest interstate/highway using Overpass API
def get_nearest_highway(lat, lon):
    try:
        # Overpass API query to find nearby highways/interstates
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        (
          way(around:5000,{lat},{lon})["highway"~"motorway|trunk|primary|secondary|tertiary"];
        );
        out center;
        """
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        if 'elements' in data and len(data['elements']) > 0:
            # Find the closest highway/interstate
            min_distance = float('inf')
            nearest_highway = "Unknown"
            nearest_coords = (0, 0)

            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    highway_name = element['tags']['name']
                    highway_lat = element['center']['lat']
                    highway_lon = element['center']['lon']

                    # Calculate the distance
                    dist_miles = geodesic((lat, lon), (highway_lat, highway_lon)).miles

                    if dist_miles < min_distance:
                        min_distance = dist_miles
                        nearest_highway = highway_name
                        nearest_coords = (highway_lat, highway_lon)

            return nearest_highway, round(min_distance, 2)
        else:
            return "No nearby highway", "N/A"
    
    except Exception as e:
        print(f"Error fetching highway data: {e}")
        return "N/A", "N/A"

# Apply functions to DataFrame
df['County'], df['ZIP Code'], df['City'], df['Road Name'] = zip(*df.apply(lambda row: get_location_info(row['Latitude'], row['Longitude']), axis=1))
df['Nearest Highway'], df['Distance to Highway (miles)'] = zip(*df.apply(lambda row: get_nearest_highway(row['Latitude'], row['Longitude']), axis=1))

# Filter out rows that are not in Tennessee
df = df[df['County'] != 'Out of Tennessee']

# Save the updated DataFrame
updated_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_Location\park_highway_data.csv"
df.to_csv(updated_file_path, index=False)

print(f"Updated file saved with County, ZIP Code, City Name, Road Name, Nearest Highway, and Distance to Highway as '{updated_file_path}'")
