import os
import pandas as pd

# Define file paths
folder_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\google"
combined_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\parking.csv"
duplicate_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\dup_park.csv"
cleaned_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\park_clean.csv"
truck_filtered_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\park_truck_filtered.csv"

# Step 1: Combine all CSV files into one DataFrame
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {folder_path}")

# Read and combine all CSV files
combined_df = pd.concat([pd.read_csv(os.path.join(folder_path, file)) for file in csv_files], ignore_index=True)
combined_df.to_csv(combined_file_path, index=False)
print(f"Combined file saved as '{combined_file_path}'")

# Step 2: Identify and save duplicate locations based on Latitude and Longitude
duplicate_df = combined_df[combined_df.duplicated(subset=['Latitude', 'Longitude'], keep=False)]
duplicate_df.to_csv(duplicate_file_path, index=False)
print(f"Duplicate locations saved as '{duplicate_file_path}'")

# Step 3: Filter rows where "Name" or "Detail_URL" contains "truck" (case-insensitive)
if 'Name' in combined_df.columns and 'Detail_URL' in combined_df.columns:
    truck_filtered_df = combined_df[
        combined_df[['Detail_URL']].apply(lambda row: row.astype(str).str.contains("truck", case=False, na=False).any(), axis=1)
    ]

    # Save the truck-filtered DataFrame before removing duplicates
    truck_filtered_df.to_csv(truck_filtered_file_path, index=False)
    print(f"Filtered truck parking file saved as '{truck_filtered_file_path}'")

    # Step 4: Remove duplicates based on Latitude and Longitude for truck parking
    truck_filtered_df = truck_filtered_df.drop_duplicates(subset=['Latitude', 'Longitude'], keep='first')

    # Save the cleaned truck parking DataFrame
    truck_filtered_df.to_csv(truck_filtered_file_path, index=False)
    print(f"Filtered and cleaned truck parking file saved as '{truck_filtered_file_path}'")

else:
    print("Required columns 'Name' or 'Detail_URL' not found in the dataset.")

# Step 5: Remove duplicates based on Latitude and Longitude from the full dataset
cleaned_df = combined_df.drop_duplicates(subset=['Latitude', 'Longitude'], keep='first')
cleaned_df.to_csv(cleaned_file_path, index=False)
print(f"Cleaned file saved as '{cleaned_file_path}'")




###category delete school & office
"""
# Re-import necessary libraries since the execution state was reset
import os
import pandas as pd

# Define the file paths
cleaned_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\park_clean_address.csv"
filtered_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Infrastructure\Parking_data\park_filtered.csv"

# Check if the cleaned file exists before proceeding
if not os.path.exists(cleaned_file_path):
    raise FileNotFoundError(f"File not found: {cleaned_file_path}")

# Load the cleaned dataset
cleaned_df = pd.read_csv(cleaned_file_path)


# Remove rows where 'Category' contains 'school' or 'office' (case-insensitive)
filtered_df = cleaned_df[~cleaned_df['Category'].str.contains("school|office|", case=False, na=False)]

# Save the filtered DataFrame
filtered_df.to_csv(filtered_file_path, index=False)

print(f"Filtered file (excluding 'school' and 'office') saved as '{filtered_file_path}'")

"""
