import pandas as pd
import os

# Load the dataset
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\business_clean.csv"
df = pd.read_csv(file_path)

# Define the output folder
output_folder = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\business_files"
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Define batch size
batch_size = 1000  # Split data into chunks of 500 rows each

# Split and save files
for i, start in enumerate(range(0, len(df), batch_size)):
    chunk = df.iloc[start:start + batch_size]  # Extract chunk
    output_file = os.path.join(output_folder, f"business_part_{i+1}.csv")  # Define file name
    chunk.to_csv(output_file, index=False)  # Save file
    print(f"Saved: {output_file}")

print("✅ Data split completed successfully!")
