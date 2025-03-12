import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the cleaned file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\business_files\business_part_7.csv"
df = pd.read_csv(file_path)

# Standardize column names (strip spaces, lowercase)
df.columns = df.columns.str.strip()

# Ensure required columns exist
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    raise ValueError("Error: Latitude and Longitude columns are required in the dataset.")

# Drop missing Latitude/Longitude values
df = df.dropna(subset=['Latitude', 'Longitude'])

# Initialize Geolocator with Nominatim
geolocator = Nominatim(user_agent="business_locator", timeout=60)

# Rate limiter to avoid API overload
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=2, max_retries=5, error_wait_seconds=5.0)

# ✅ Corrected Function with Logging & Robust Error Handling
def get_location_info(lat, lon):
    try:
        # Ensure latitude and longitude are valid numbers
        if pd.isna(lat) or pd.isna(lon):
            return 'Invalid', 'N/A', 'N/A'
        
        # Reverse geocode the coordinates
        location = geocode((lat, lon), language='en')
        
        if location:
            address = location.raw.get('address', {})
            state = address.get('state', 'N/A')

            # ✅ Only keep locations in Tennessee
            if state == 'Tennessee':
                county = address.get('county', 'N/A')
                zip_code = address.get('postcode', 'N/A')
                city = address.get('city', address.get('town', address.get('village', 'N/A')))
                return county, zip_code, city
            else:
                print(f"Skipping non-Tennessee location: {state}")
                return 'Out of Tennessee', 'N/A', 'N/A'
        else:
            return 'No Data', 'N/A', 'N/A'
    
    except Exception as e:
        print(f"Error for coordinates {lat}, {lon}: {e}")
        return 'Error', 'N/A', 'N/A'

# Apply function to each row
df['County'], df['ZIP Code'], df['City'] = zip(*df.apply(lambda row: get_location_info(row['Latitude'], row['Longitude']), axis=1))

# ✅ Remove rows that are NOT in Tennessee
df = df[df['County'] != 'Out of Tennessee']
df = df[df['County'] != 'Error']
df = df[df['County'] != 'Invalid']
df = df[df['County'] != 'No Data']

# Save the updated DataFrame
updated_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\business_files\business6_zip.csv"
df.to_csv(updated_file_path, index=False)

print(f"✅ Updated file saved: '{updated_file_path}' with only Tennessee locations")

