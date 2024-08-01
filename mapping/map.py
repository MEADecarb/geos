import streamlit as st
import folium
import requests
import pandas as pd
from streamlit_folium import st_folium

# URLs to your GeoJSON files and CSV on GitHub
geojson_url1 = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/Enough_Act_Child_Poverty_Census_Tracts_-2847962131010073922%20(1).geojson'
geojson_url2 = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/Enough_Act_School_Locations.geojson'
geojson_url3 = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/MDHB550CensusTracts%20(1).geojson'
csv_url = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/MDOTSolar.csv'

# Create a base map
m = folium.Map(location=[39.2904, -76.6122], zoom_start=10)  # Replace latitude and longitude with your desired center coordinates

# Function to add GeoJSON to the map with custom style
def add_geojson_to_map(url, map_obj, layer_name, color):
    response = requests.get(url)
    data = response.json()
    folium.GeoJson(
        data,
        name=layer_name,
        style_function=lambda x: {'color': color, 'weight': 2}
    ).add_to(map_obj)

# Add each GeoJSON layer to the map with custom colors
add_geojson_to_map(geojson_url1, m, 'ENOUGH ACT Census Tracts', 'purple')
add_geojson_to_map(geojson_url2, m, 'School Locations', 'yellow')  # Default color for School Locations
add_geojson_to_map(geojson_url3, m, 'HB550 Census Tracts', 'orange')

# Function to add point layer from CSV with custom icon
def add_point_layer_from_csv(url, map_obj, icon_url):
    data = pd.read_csv(url)
    for index, row in data.iterrows():
        folium.Marker(
            location=[row['lat'], row['long']],
            icon=folium.CustomIcon(icon_url, icon_size=(30, 30)),
            popup=row['MDOT Location']  
        ).add_to(map_obj)

# URL to your custom icon
icon_url = 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Sunshine_icon.png'

# Add the point layer to the map
add_point_layer_from_csv(csv_url, m, icon_url)

# Add layer control to the map
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st.title('Interactive Map with GeoJSON Layers')
st_folium(m, width=700, height=500)
