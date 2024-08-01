import streamlit as st
import folium
import requests
from folium import GeoJson
from streamlit_folium import st_folium

# List of GeoJSON files in the GitHub repository
geojson_files = [
    "Enough_CP_ct.GEOJSON",
    "Enough_Act_School_Locations.geojson",
    "MDHB550CensusTracts.geojson",
]

# Function to get raw GitHub URL for a GeoJSON file
def get_raw_github_url(file_name):
    return f"https://raw.githubusercontent.com/MEADecarb/geos/main/data/{file_name}"

# Streamlit app
st.title("Folium Map with GeoJSON Data")

# Create a Folium map
m = folium.Map(location=[39.5, -98.35], zoom_start=4)

# Add each GeoJSON file to the map
for file_name in geojson_files:
    geojson_url = get_raw_github_url(file_name)
    response = requests.get(geojson_url)
    
    if response.status_code == 200:
        try:
            geojson_data = response.json()
            GeoJson(geojson_data, name=file_name).add_to(m)
        except ValueError as e:
            st.error(f"Error decoding JSON for {file_name}: {e}")
            st.text(f"Response content: {response.text[:200]}")  # Display first 200 characters of the response
    else:
        st.error(f"Failed to load {file_name}: HTTP {response.status_code}")

# Display the map in Streamlit
st_folium(m, width=700, height=500)
