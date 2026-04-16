python
import pandas as pd
import folium
import requests

# Load public transportation data
transport_data = pd.read_csv('public_transportation_data.csv')

# Load air quality data through API
def fetch_aqi_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

api_url = 'https://api.example.com/air_quality'
aqi_data = fetch_aqi_data(api_url)

if aqi_data:
    for record in aqi_data:
        # Process AQI data
        location = record['location']
        aqi = record['AQI']
        pollutants = record['pollutants']
        # Print example data
        print(f"Location: {location}, AQI: {aqi}, Pollutants: {pollutants}")

# Merge datasets - assuming both have a 'location' and 'date' column
merged_data = pd.merge(transport_data, pd.DataFrame(aqi_data), on=['location', 'date'])

# Generate heatmap
map = folium.Map(location=[24.4539, 54.3773], zoom_start=10)
for index, row in merged_data.iterrows():
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        radius=row['ridership'] * 10,  # Scale for visualization
        color='blue' if row['AQI'] <= 50 else 'red',
        fill=True,
        fill_color='blue' if row['AQI'] <= 50 else 'red',
    ).add_to(map)

map.save('transport_aqi_heatmap.html')

print("Heatmap saved as transport_aqi_heatmap.html")
