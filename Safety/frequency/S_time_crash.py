import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Collision_Time' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Collision_Time' and 'Total' columns.")

# Aggregate crash frequency by time
time_crash_data = df.groupby("Collision_Time")["Total"].sum().reset_index()

# Sort by time to ensure correct order
time_crash_data = time_crash_data.sort_values(by="Collision_Time")

# Create line chart
fig = px.line(
    time_crash_data, 
    x="Collision_Time", 
    y="Total", 
    title="Crash Frequency Trends Over Time",
    labels={"Total": "Total Crashes", "Collision_Time": "Time"},
    markers=True,  # Adds points on the line for better visibility
    line_shape="spline"  # Makes the line smoother
)

# Save as an interactive HTML file
fig.write_html("Truck_crash_trends_by_time.html")

print("Line graph saved as Truck_crash_trends_by_time.html")


########################### Trend of Crash frequency
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Check if required columns exist
if 'Collision_Time' not in df.columns or 'Total' not in df.columns:
    raise ValueError("Data must contain 'Collision_Time' and 'Total' columns.")

# Convert 'Collision_Time' to datetime format and extract only the hour
df["Collision_Time"] = pd.to_datetime(df["Collision_Time"], format="%H:%M").dt.hour  # Extracting only hour

# Aggregate crash frequency by hour
hourly_crash_data = df.groupby("Collision_Time")["Total"].sum().reset_index()

# Sort by hour to ensure correct order
hourly_crash_data = hourly_crash_data.sort_values(by="Collision_Time")

# Create the plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=hourly_crash_data, x="Collision_Time", y="Total", marker="o", linewidth=2, color="b")

# Formatting
plt.title("Truck Crash Frequency Trends by Hour", fontsize=14, fontweight='bold')
plt.xlabel("Hour of a Day", fontsize=12)
plt.ylabel("Total Crashes", fontsize=12)

# Set x-axis to show whole numbers from 0 to 24
plt.xticks(ticks=range(0, 25), labels=[str(h) for h in range(0, 25)], rotation=45, ha="right")

plt.grid(True, linestyle="--", alpha=0.7)

# Show the plot
plt.show()



#################################################### cross table day vs hour *** need html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Convert 'Collision_Date' to datetime format and extract Day of Week
df["Collision_Date"] = pd.to_datetime(df["Collision_Date"])
df["Day"] = df["Collision_Date"].dt.day_name()  # Extract full day name (Monday, Tuesday, etc.)

# Convert 'Collision_Time' to datetime format and extract the Hour
df["Collision_Time"] = pd.to_datetime(df["Collision_Time"], format="%H:%M").dt.hour

# Aggregate crash frequency by Hour (rows) and Day (columns)
cross_table = df.pivot_table(values="Total", index="Collision_Time", columns="Day", aggfunc="sum", fill_value=0)

# Reorder days for proper weekday sorting
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
cross_table = cross_table[ordered_days]

# Plot heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(cross_table, cmap="Reds", annot=True, fmt="d", linewidths=0.5)

# Formatting
plt.title("", fontsize=14, fontweight="bold")
plt.xlabel("Day of the Week", fontsize=12)
plt.ylabel("Hour of the Day", fontsize=12)
plt.xticks(rotation=45)
plt.yticks(ticks=range(0, 24), labels=[str(h) for h in range(0, 24)], rotation=0)  # Ensure y-axis shows whole numbers

# Show the plot
plt.show()

"""
#html version
import pandas as pd
import plotly.express as px
import os

# Load dataset
file_path = r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv"
df = pd.read_csv(file_path)

# Remove spaces in column names
df.columns = df.columns.str.strip()

# Convert 'Collision_Time' to datetime format and extract the hour only
df["Collision_Time"] = pd.to_datetime(df["Collision_Time"], format="%H:%M", errors="coerce").dt.hour

# Ensure 'Day' column is in full weekday format
day_mapping = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday",
               "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
df["Day"] = df["Day"].map(day_mapping)

# Create pivot table (Hourly summary)
cross_table = df.pivot_table(values="Total", index="Collision_Time", columns="Day", aggfunc="sum", fill_value=0)

# Reorder days properly
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
cross_table = cross_table[ordered_days]

# Create heatmap using Plotly
fig = px.imshow(
    cross_table,
    labels={"x": "Day of the Week", "y": "Hour of the Day", "color": "Crash Count"},
    color_continuous_scale="Reds",
    title="Crash Frequency Heatmap by Hour & Day"
)

# Format axes
fig.update_xaxes(tickangle=45)
fig.update_yaxes(tickmode="array", tickvals=list(range(24)), title="Hour of the Day")

# Save the heatmap as an HTML file
output_dir = r"D:\Mobility Report & Dashboard\Dashboard_Code\Safety"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
output_path = os.path.join(output_dir, "Crash_Frequency_Heatmap.html")
fig.write_html(output_path)

print(f"✅ Interactive heatmap saved at: {output_path}")
"""



#################### Crash Day Percentage need HTML
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(r"D:\Mobility Report & Dashboard\TITAN_Data\Medium_Heavy_Truck_Crash_2024.csv")

# Convert 'Total' to numeric
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# Drop missing values in relevant columns
df = df.dropna(subset=["Day", "Total"])

# Aggregate crash counts by day
day_crash_counts = df.groupby("Day")["Total"].sum().reset_index()

# Plot bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=day_crash_counts, x="Day", y="Total", palette="Reds")

# Formatting
plt.title("", fontsize=14, fontweight="bold")
plt.xlabel("Day of the Week", fontsize=12)
plt.ylabel("Total Crashes", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the plot
plt.show()
