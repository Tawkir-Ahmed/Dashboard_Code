############ County all
import pandas as pd
import plotly.express as px

# Load the CSV file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated.csv"
df = pd.read_csv(file_path)

# Check if the 'County' column exists
if 'County' in df.columns:
    # Remove rows where 'County' contains the word "Country"
    df_filtered = df[~df['County'].str.contains("Country", case=False, na=False)]

    # Count occurrences of each county after filtering
    county_counts = df_filtered['County'].value_counts().nlargest(10)  # Get top 10 counties

    # Remove the word "County" from the x-axis labels
    county_labels = [name.replace("County", "").strip() for name in county_counts.index]

    # Convert to DataFrame for better handling
    df_chart = pd.DataFrame({'County': county_labels, 'Establishments': county_counts.values})

    # Create bar chart using Plotly with a color bar
    fig = px.bar(
        df_chart, 
        x='County', 
        y='Establishments', 
        labels={'x': 'County', 'y': 'Number of Establishments'},  # Updated y-axis title
        title="Top 10 County Distribution",
        text='Establishments',  # Display count on bars
        color='County',  # Assign different colors to each county
        color_discrete_sequence=px.colors.qualitative.Plotly  # Use a predefined color set
    )

    fig.update_traces(textposition='outside')  # Position text outside bars

    fig.update_layout(
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        showlegend=True  # Enable the color bar (legend)
    )

    # Save as an HTML file
    output_html = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\top_10_counties_bar_chart.html"
    fig.write_html(output_html)

    print(f"Bar chart saved as {output_html}")
else:
    print("Column 'County' not found in the dataset.")





############ County- trasnportation and logistic
import pandas as pd
import plotly.express as px

# Load the CSV file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated.csv"
df = pd.read_csv(file_path)

# Check if both 'Class' and 'County' columns exist
if 'Class' in df.columns and 'County' in df.columns:
    # Filter data for "Transportation and Warehousing"
    df_filtered = df[df['Class'] == "Transportation and Warehousing"]

    # Count occurrences of each county after filtering
    county_counts = df_filtered['County'].value_counts().nlargest(10)  # Get top 10 counties

    # Remove the word "County" from the x-axis labels
    county_labels = [name.replace("County", "").strip() for name in county_counts.index]

    # Convert to DataFrame for better Plotly handling
    df_chart = pd.DataFrame({'County': county_labels, 'Establishments': county_counts.values})

    # Define a light red color (adjust if needed)
    light_red = "#FF6F61"  # Light Red color

    # Create bar chart using Plotly with a light red color
    fig = px.bar(
        df_chart, 
        x='County', 
        y='Establishments', 
        labels={'x': 'County', 'y': 'Number of Establishments'},  # Updated y-axis title
        title="Top 10 Counties for Transportation and Warehousing",
        text='Establishments'  # Display count on bars
    )

    fig.update_traces(
        textposition='outside',
        marker_color=light_red  # Apply the light red color
    )

    fig.update_layout(
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        showlegend=False  # Remove the sidebar (color legend)
    )

    # Save as an HTML file
    output_html = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\top_10_transportation_warehousing.html"
    fig.write_html(output_html)

    print(f"Bar chart saved as {output_html}")
else:
    print("Column 'Class' or 'County' not found in the dataset.")


############ County- Manufacturing and Distribution
import pandas as pd
import plotly.express as px

# Load the CSV file
file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated.csv"
df = pd.read_csv(file_path)

# Check if both 'Class' and 'County' columns exist
if 'Class' in df.columns and 'County' in df.columns:
    # Filter data for "Manufacturing and Industrial"
    df_filtered = df[df['Class'] == "Manufacturing and Industrial"]

    # Count occurrences of each county after filtering
    county_counts = df_filtered['County'].value_counts().nlargest(10)  # Get top 10 counties

    # Remove the word "County" from the x-axis labels
    county_labels = [name.replace("County", "").strip() for name in county_counts.index]

    # Convert to DataFrame for better Plotly handling
    df_chart = pd.DataFrame({'County': county_labels, 'Establishments': county_counts.values})

    # Define a single color (change the hex code if you want a different color)
    single_color = "#f59042"  # Example: Blue

    # Create bar chart using Plotly with a single color
    fig = px.bar(
        df_chart, 
        x='County', 
        y='Establishments', 
        labels={'x': 'County', 'y': 'Number of Establishments'},  # Updated y-axis title
        title="Top 10 Counties for Manufacturing and Industries",
        text='Establishments',  # Display count on bars
    )

    fig.update_traces(
        textposition='outside',
        marker_color=single_color  # Apply the single color to all bars
    )

    fig.update_layout(
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        showlegend=False  # Ensure the color bar/legend is removed
    )

    # Save as an HTML file
    output_html = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\top_10_manufacturing_industries.html"
    fig.write_html(output_html)

    print(f"Bar chart saved as {output_html}")
else:
    print("Column 'Class' or 'County' not found in the dataset.")







import requests
from bs4 import BeautifulSoup

# Define the URL and headers
url = "https://truckparkingclub.com/user/kpg282"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Define file path for saving the HTML content
    file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\scraped_page.html"

    # Save the HTML content
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    print(f"Webpage saved as {file_path}")
else:
    print("Failed to fetch the webpage.")






from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode

# ✅ Replace with your actual ChromeDriver path
chrome_driver_path = r"C:\WebDriver\chromedriver.exe"  
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the website
url = "https://truckparkingclub.com/user/kpg282"
driver.get(url)

# Extract page source after JavaScript renders
page_source = driver.page_source

# Parse using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Extract parking location names and prices
parking_data = []
for parking in soup.find_all("div", class_="parking-card"):  # Update class name if needed
    location = parking.find("h3").get_text(strip=True) if parking.find("h3") else "No Location"
    price = parking.find("span", class_="price").get_text(strip=True) if parking.find("span", class_="price") else "No Price"
    
    parking_data.append({"Location": location, "Price": price})

# Close the Selenium WebDriver
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(parking_data)

# Define file path for saving extracted data
csv_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\parking_data.csv"

# Save as CSV
df.to_csv(csv_file_path, index=False, encoding="utf-8")

print(f"Parking data saved as {csv_file_path}")
