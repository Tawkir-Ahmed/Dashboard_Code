import os
import pandas as pd

# Define file paths
folder_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\Factories"
combined_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories.csv"
duplicate_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\dup_factories.csv"
cleaned_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_clean.csv"

# Step 1: Combine all CSV files into one DataFrame
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {folder_path}")

# Read and combine all CSV files
combined_df = pd.concat([pd.read_csv(os.path.join(folder_path, file)) for file in csv_files], ignore_index=True)
combined_df.to_csv(combined_file_path, index=False)
print(f"Combined file saved as '{combined_file_path}'")

# Step 2: Identify and save duplicate locations based on Latitude and Longitude
if 'Latitude' in combined_df.columns and 'Longitude' in combined_df.columns:
    duplicate_df = combined_df[combined_df.duplicated(subset=['Latitude', 'Longitude'], keep=False)]
    duplicate_df.to_csv(duplicate_file_path, index=False)
    print(f"Duplicate locations saved as '{duplicate_file_path}'")

# Step 3: Remove duplicates based on Latitude and Longitude from the full dataset
if 'Latitude' in combined_df.columns and 'Longitude' in combined_df.columns:
    cleaned_df = combined_df.drop_duplicates(subset=['Latitude', 'Longitude'], keep='first')
    cleaned_df.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned file saved as '{cleaned_file_path}'")
