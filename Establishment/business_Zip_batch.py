import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the cleaned file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\business_files\business_part_1.csv"
df = pd.read_csv(file_path)

# Check if Latitude and Longitude columns exist
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    raise ValueError("Latitude and Longitude columns are required in the dataset.")

# Drop missing Latitude/Longitude values
df = df.dropna(subset=['Latitude', 'Longitude'])

# Initialize Geolocator with increased timeout
geolocator = Nominatim(user_agent="business_locator", timeout=30)

# Rate limiter with increased delay
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=2, max_retries=5, error_wait_seconds=5.0)

# Function to get County from Latitude and Longitude
def get_county(lat, lon):
    try:
        location = geocode((lat, lon), language='en')
        if location:
            address = location.raw.get('address', {})
            state = address.get('state', 'N/A')

            # Only keep locations in Tennessee
            if state == 'Tennessee':
                county = address.get('county', 'N/A')
                return county
            else:
                print(f"Skipping non-Tennessee location: {state}")
                return 'Out of Tennessee'
    except Exception as e:
        print(f"Error for coordinates {lat}, {lon}: {e}")
        return 'Error'

# Apply function and store results
df['County'] = df.apply(lambda row: get_county(row['Latitude'], row['Longitude']), axis=1)

# Filter out rows that are not in Tennessee
df = df[df['County'] != 'Out of Tennessee']
df = df[df['County'] != 'Error']  # Remove failed lookups

# Save the updated DataFrame
updated_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\business_part_2_tennessee.csv"
df.to_csv(updated_file_path, index=False)

print(f"✅ Updated file saved: '{updated_file_path}' with only Tennessee locations")
