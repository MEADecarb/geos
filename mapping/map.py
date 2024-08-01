import folium
import requests
import json

# URLs to your GeoJSON files on GitHub
geojson_url1 = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/Enough_Act_Child_Poverty_Census_Tracts_-2847962131010073922%20(1).geojson'
geojson_url2 = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/Enough_Act_School_Locations.geojson'
geojson_url3 = 'https://raw.githubusercontent.com/MEADecarb/geos/main/data/MDHB550CensusTracts%20(1).geojson'

# Create a base map
m = folium.Map(location=[39.2904, -76.6122], zoom_start=10)  # Replace latitude and longitude with your desired center coordinates

# Function to add GeoJSON to the map
def add_geojson_to_map(url, map_obj, layer_name):
    response = requests.get(url)
    data = response.json()
    folium.GeoJson(data, name=layer_name).add_to(map_obj)

# Add each GeoJSON layer to the map
add_geojson_to_map(geojson_url1, m, 'Child Poverty Census Tracts')
add_geojson_to_map(geojson_url2, m, 'School Locations')
add_geojson_to_map(geojson_url3, m, 'Census Tracts')

# Add layer control to the map
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('map.html')

# To display the map in a Jupyter Notebook
m
