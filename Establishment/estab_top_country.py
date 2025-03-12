import pandas as pd
import plotly.express as px

# 📌 Load the data
data_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\Establishment_data\factories_files\all_factories_zip.csv"
df = pd.read_csv(data_path)

# 📌 Ensure required columns exist
required_columns = ['County']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# 📌 Group by County and count the number of businesses in each county
county_counts = df['County'].value_counts().reset_index()
county_counts.columns = ['County', 'BusinessCount']

# 📌 Sort by BusinessCount in descending order and select top 10 counties
top_10_counties = county_counts.sort_values(by='BusinessCount', ascending=False).head(10)

# 📌 Create a bar chart using Plotly
fig = px.bar(
    top_10_counties,
    x='County',
    y='BusinessCount',
    title='Top 10 Counties by Number of Businesses',
    labels={'County': 'County', 'BusinessCount': 'Number of Businesses'},
    color='BusinessCount',
    color_continuous_scale='Blues',
    template='plotly_dark'
)

# 📌 Save the chart as an HTML file
output_html_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\top_10_counties_bar_chart.html"
fig.write_html(output_html_path)

print(f"✅ Top 10 counties bar chart saved as HTML at: {output_html_path}")
