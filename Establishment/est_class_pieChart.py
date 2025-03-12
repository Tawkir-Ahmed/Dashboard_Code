import pandas as pd
import plotly.express as px

# Load the CSV file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated.csv"
df = pd.read_csv(file_path)

# Check if the 'Class' column exists
if 'Class' in df.columns:
    # Count the occurrences of each category in the "Class" column
    class_counts = df['Class'].value_counts()

    # Create a pie chart using plotly
    fig = px.pie(
        names=class_counts.index, 
        values=class_counts.values, 
        title="Distribution of Establishment Categories"
    )

    # Save the plot as an HTML file
    output_html = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\class_pie_chart.html"
    fig.write_html(output_html)

    print(f"Pie chart saved as {output_html}")
else:
    print("Column 'Class' not found in the dataset.")


###################################graph for presentaiton
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated.csv"
df = pd.read_csv(file_path)

# Check if the 'Class' column exists
if 'Class' in df.columns:
    # Count the occurrences of each category in the "Class" column
    class_counts = df['Class'].value_counts()

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(class_counts.index, class_counts.values, color='skyblue', edgecolor='black')

    # Add percentage labels above bars
    total = class_counts.sum()
    for bar, count in zip(bars, class_counts.values):
        percentage = (count / total) * 100
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{percentage:.1f}%', 
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Labels and title
    plt.xlabel("Class Categories", fontsize=14)
    plt.ylabel("Count", fontsize=14)
    plt.title("", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.show()
else:
    print("Column 'Class' not found in the dataset.")
