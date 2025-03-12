import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the cleaned file
file_path = r"D:\Mobility Report & Dashboard\EV_Charging_data\charge_clean.csv"
df = pd.read_csv(file_path)

# Check if Latitude and Longitude columns exist
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    raise ValueError("Latitude and Longitude columns are required in the dataset.")

# Initialize Geolocator with Nominatim
geolocator = Nominatim(user_agent="ev_charging_locator")

# Rate limiter to avoid request overload and respect Nominatim usage policy
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1, max_retries=3, error_wait_seconds=2.0)

# Function to get County, ZIP Code, and City Name from Latitude and Longitude
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
                city = address.get('city', address.get('town', address.get('village', 'N/A')))  # Check for city, town, or village
                
                return county, zip_code, city
            else:
                print(f"Skipping non-Tennessee location: {state}")
                return 'Out of Tennessee', 'N/A', 'N/A'
    except Exception as e:
        print(f"Error: {e}")
    return 'N/A', 'N/A', 'N/A'

# Apply function to each row and add County, ZIP Code, and City Name columns
df['County'], df['ZIP Code'], df['City'] = zip(*df.apply(lambda row: get_location_info(row['Latitude'], row['Longitude']), axis=1))

# Filter out rows that are not in Tennessee
df = df[df['County'] != 'Out of Tennessee']

# Save the updated DataFrame with County, ZIP Code, and City Name
updated_file_path = r"D:\Mobility Report & Dashboard\EV_Charging_data\charge_county_zip_city.csv"
df.to_csv(updated_file_path, index=False)

print(f"Updated file saved with County, ZIP Code, and City Name as '{updated_file_path}'")


