import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Relation_To_Junction' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Relation_To_Junction' and 'Total' columns.")

# Group by 'Relation_To_Junction' and sum 'Total' crashes for each junction type
junction_crash_data = df.groupby('Relation_To_Junction').agg({'Total': 'sum'}).reset_index()

# Sort the data from highest to lowest based on the 'Total' crashes
junction_crash_data = junction_crash_data.sort_values(by='Total', ascending=False)

# Select the top 10 entries with the highest total crashes
top_10_junctions = junction_crash_data.head(10)

# Create bar plot for total crashes by Relation_To_Junction
fig = px.bar(
    top_10_junctions,
    x="Relation_To_Junction",  # Junction types on the x-axis
    y="Total",  # Total crashes on the y-axis
    title="Top 10 Truck Crashes by Junction Type",
    labels={"Total": "Crash Frequency", "Relation_To_Junction": "Junction Type"},
    color="Relation_To_Junction",  # Optional: Color bars by Junction Type
    text="Total"  # Optional: Show total crash values on the bars
)

# Show the plot
fig.show()

# Save the plot as an interactive HTML file
fig.write_html("Top_10_Total_crashes_by_Junction_Type_barplot.html")

print("Bar plot saved as Top_10_Total_crashes_by_Junction_Type_barplot.html")


########################## Top 10 road  need html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Roadway_Name' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Roadway_Name' and 'Total' columns.")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Standardizing Roadway Names
roadway_name_corrections = {
    "S. U.s. Highway 51": "US-51",
    "Us-27 S": "US-27",
    "I240 RD": "I-240",
    "Battlefield Dr": "Battlefield Drive",
    "Tn-95": "TN-95",
    "I 40": "I-40",
    "I 75": "I-75",
    "I 24": "I-24",
    "I 65": "I-65",
    "Tn-240": "TN-240",
    "Us 64": "US-64",
    "S Highway 51": "US-51",
    "Us 41": "US-41",
    "101st Airborne Division Parkway PKWY": "TN-374"
}

df["Roadway_Name"] = df["Roadway_Name"].replace(roadway_name_corrections)

# Classify roadways into Interstates and Highways
df["Road_Type"] = df["Roadway_Name"].apply(lambda x: "Interstate" if str(x).startswith("I-") else "Highway")

# Group by 'Roadway_Name' and sum 'Total' crashes for each road
roadway_crash_data = df.groupby(["Roadway_Name", "Road_Type"])["Total"].sum().reset_index()

# Separate data for Interstates and Highways
interstate_crashes = roadway_crash_data[roadway_crash_data["Road_Type"] == "Interstate"].sort_values(by="Total", ascending=False).head(5)
highway_crashes = roadway_crash_data[roadway_crash_data["Road_Type"] == "Highway"].sort_values(by="Total", ascending=False).head(5)

# Create bar chart for Interstates
plt.figure(figsize=(10, 5))
sns.barplot(data=interstate_crashes, x="Total", y="Roadway_Name", palette="Blues_r", orient="h")

# Formatting for whole numbers in x-axis
plt.xticks(np.arange(0, interstate_crashes["Total"].max() + 1, step=1))  # Whole numbers only

plt.title("Top 5 Interstates by Total Truck Crashes", fontsize=14, fontweight="bold")
plt.xlabel("Total Crashes", fontsize=12)
plt.ylabel("Interstate", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# Create bar chart for Highways
plt.figure(figsize=(10, 5))
sns.barplot(data=highway_crashes, x="Total", y="Roadway_Name", palette="Reds_r", orient="h")

# Formatting for whole numbers in x-axis
plt.xticks(np.arange(0, highway_crashes["Total"].max() + 1, step=1))  # Whole numbers only

plt.title("Top 5 Highways by Total Truck Crashes", fontsize=14, fontweight="bold")
plt.xlabel("Total Crashes", fontsize=12)
plt.ylabel("Highway", fontsize=12)
plt.yticks(rotation=45, ha="right")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

"""
#Html
import pandas as pd
import plotly.express as px
import os

# Load dataset
file_path = r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv"
df = pd.read_csv(file_path)

# Check if required columns exist
if 'Roadway_Name' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Roadway_Name' and 'Total' columns.")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Standardizing Roadway Names
roadway_name_corrections = {
    "S. U.s. Highway 51": "US-51",
    "Us-27 S": "US-27",
    "I240 RD": "I-240",
    "Battlefield Dr": "Battlefield Drive",
    "Tn-95": "TN-95",
    "I 40": "I-40",
    "I 75": "I-75",
    "I 24": "I-24",
    "I 65": "I-65",
    "Tn-240": "TN-240",
    "Us 64": "US-64",
    "S Highway 51": "US-51",
    "Us 41": "US-41",
    "101st Airborne Division Parkway PKWY": "TN-374"
}
df["Roadway_Name"] = df["Roadway_Name"].replace(roadway_name_corrections)

# Classify roadways into Interstates and Highways
df["Road_Type"] = df["Roadway_Name"].apply(lambda x: "Interstate" if str(x).startswith("I-") else "Highway")

# Group by 'Roadway_Name' and sum 'Total' crashes for each road
roadway_crash_data = df.groupby(["Roadway_Name", "Road_Type"])["Total"].sum().reset_index()

# Separate data for Interstates and Highways
interstate_crashes = roadway_crash_data[roadway_crash_data["Road_Type"] == "Interstate"].sort_values(by="Total", ascending=False).head(5)
highway_crashes = roadway_crash_data[roadway_crash_data["Road_Type"] == "Highway"].sort_values(by="Total", ascending=False).head(5)

# ✅ **Create interactive bar chart for Interstates**
fig_interstates = px.bar(
    interstate_crashes,
    x="Total",
    y="Roadway_Name",
    orientation="h",
    title="Top 5 Interstates by Total Truck Crashes",
    labels={"Total": "Total Crashes", "Roadway_Name": "Interstate"},
    color="Total",
    color_continuous_scale="Reds"
)

# ✅ **Create interactive bar chart for Highways**
fig_highways = px.bar(
    highway_crashes,
    x="Total",
    y="Roadway_Name",
    orientation="h",
    title="Top 5 Highways by Total Truck Crashes",
    labels={"Total": "Total Crashes", "Roadway_Name": "Highway"},
    color="Total",
    color_continuous_scale="Reds"
)

# ✅ **Save figures as an HTML file**
output_dir = r"D:\Mobility Report & Dashboard\Dashboard_Code\Safety"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

output_path_interstates = os.path.join(output_dir, "Interstate_Crashes.html")
output_path_highways = os.path.join(output_dir, "Highway_Crashes.html")

fig_interstates.write_html(output_path_interstates)
fig_highways.write_html(output_path_highways)

print(f"✅ Interstate crash chart saved at: {output_path_interstates}")
print(f"✅ Highway crash chart saved at: {output_path_highways}")

"""

########################### Road Interstates with junction need html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Roadway_Name' not in df.columns or 'Relation_To_Junction' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Roadway_Name', 'Relation_To_Junction', and 'Total' columns.")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Filter data for all interstates (I-40, I-65, I-24, etc.)
interstate_data = df[df["Roadway_Name"].str.startswith("I-", na=False)]

# Aggregate crashes by Relation_To_Junction
junction_crash_counts = interstate_data.groupby("Relation_To_Junction")["Total"].sum().reset_index()

# Sort in descending order of crashes
junction_crash_counts = junction_crash_counts.sort_values(by="Total", ascending=False)

# Create bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=junction_crash_counts, x="Total", y="Relation_To_Junction", palette="Blues_r", orient="h")

# Formatting
plt.title("Total Crashes on All Interstates by Junction Type", fontsize=14, fontweight="bold")
plt.xlabel("Total Crashes", fontsize=12)
plt.ylabel("Junction Type", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.yticks(rotation=45, ha="right")

# Ensure x-axis shows whole numbers only with a gap of 5
max_value = int(junction_crash_counts["Total"].max())  
plt.xticks(np.arange(0, max_value + 1, step=5))  

# Show the plot
plt.show()

"""
#Html file
import pandas as pd
import plotly.express as px
import os

# Load dataset
file_path = r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv"
df = pd.read_csv(file_path)

# Check if required columns exist
if 'Roadway_Name' not in df.columns or 'Relation_To_Junction' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Roadway_Name', 'Relation_To_Junction', and 'Total' columns.")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Filter data for all interstates (I-40, I-65, I-24, etc.)
interstate_data = df[df["Roadway_Name"].str.startswith("I-", na=False)]

# Aggregate crashes by Relation_To_Junction
junction_crash_counts = interstate_data.groupby("Relation_To_Junction")["Total"].sum().reset_index()

# Sort in descending order of crashes
junction_crash_counts = junction_crash_counts.sort_values(by="Total", ascending=False)

# ✅ **Create interactive bar chart**
fig = px.bar(
    junction_crash_counts,
    x="Total",
    y="Relation_To_Junction",
    orientation="h",
    title="Total Crashes on All Interstates by Junction Type",
    labels={"Total": "Total Crashes", "Relation_To_Junction": "Junction Type"},
    color="Total",
    color_continuous_scale="Reds"
)

# ✅ **Save figure as an HTML file**
output_dir = r"D:\Mobility Report & Dashboard\Dashboard_Code\Safety"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

output_path = os.path.join(output_dir, "Interstate_Junction_Crashes.html")
fig.write_html(output_path)

print(f"✅ Interactive bar chart saved at: {output_path}")

"""

#################### Road Highways with junction need html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024_I.csv")

# Check if required columns exist
if 'Relation_To_Junction' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Relation_To_Junction' and 'Total' columns.")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Aggregate crashes by Relation_To_Junction
junction_crash_counts = df.groupby("Relation_To_Junction")["Total"].sum().reset_index()

# Sort in descending order of crashes
junction_crash_counts = junction_crash_counts.sort_values(by="Total", ascending=False)

# Create bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=junction_crash_counts, x="Total", y="Relation_To_Junction", palette="Reds_r", orient="h")

# Formatting
plt.title("Total Crashes by Junction Type", fontsize=14, fontweight="bold")
plt.xlabel("Total Crashes", fontsize=12)
plt.ylabel("Junction Type", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.yticks(rotation=45, ha="right")

# Ensure x-axis shows whole numbers only with a gap of 5
max_value = int(junction_crash_counts["Total"].max())
plt.xticks(np.arange(0, max_value + 1, step=5))

# Show the plot
plt.show()

"""
#Html
import pandas as pd
import plotly.express as px
import os

# Load dataset
file_path = r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024_I.csv"
df = pd.read_csv(file_path)

# Check if required columns exist
if 'Relation_To_Junction' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Relation_To_Junction' and 'Total' columns.")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Aggregate crashes by Relation_To_Junction
junction_crash_counts = df.groupby("Relation_To_Junction")["Total"].sum().reset_index()

# Sort in descending order of crashes
junction_crash_counts = junction_crash_counts.sort_values(by="Total", ascending=False)

# ✅ **Create interactive bar chart**
fig = px.bar(
    junction_crash_counts,
    x="Total",
    y="Relation_To_Junction",
    orientation="h",
    title="Total Crashes by Junction Type",
    labels={"Total": "Total Crashes", "Relation_To_Junction": "Junction Type"},
    color="Total",
    color_continuous_scale="Reds"
)

# ✅ **Save figure as an HTML file**
output_dir = r"D:\Mobility Report & Dashboard\Dashboard_Code\Safety"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

output_path = os.path.join(output_dir, "Highways_Junction_Crashes.html")
fig.write_html(output_path)

print(f"✅ Interactive bar chart saved at: {output_path}")

"""