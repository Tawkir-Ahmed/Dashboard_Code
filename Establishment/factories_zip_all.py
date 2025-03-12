import pandas as pd
import os

# Define file paths for all CSVs
file_paths = [
    r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\factories1_zip.csv",
    r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\factories2_zip.csv",
    r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\factories3_zip.csv",
    r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\factories4_zip.csv",
    r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\factories5_zip.csv"
]

# Load all CSVs into a list of dataframes
dfs = [pd.read_csv(file_path) for file_path in file_paths]

# Check if the column names are consistent across all files
for i, df in enumerate(dfs):
    print(f"Columns in factories{i+1}_zip:", df.columns)

# Ensure the column names are consistent (optional, if needed)
# This assumes the column names in all files should match the first one
for df in dfs[1:]:
    df.columns = dfs[0].columns  # Align column names

# Combine all the dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Define the save path for the combined CSV file
save_folder = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "all_factories_zip.csv")

# Save the combined dataframe as a CSV
combined_df.to_csv(save_path, index=False)

print(f"✅ Combined file saved at: {save_path}")
