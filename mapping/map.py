import streamlit as st
import folium
import requests
from folium import GeoJson
from streamlit_folium import st_folium

# GitHub repository URL
repo_url = "https://github.com/MEADecarb/geos/tree/main/data"

# List of GeoJSON files in the GitHub repository
geojson_files = [
    "file1.geojson",  # Replace with actual file names
    "file2.geojson",
    "file3.geojson",
]

# Function to get raw GitHub URL for a GeoJSON file
def get_raw_github_url(repo_url, file_name):
    return f"https://raw.githubusercontent.com/MEADecarb/geos/main/data/{file_name}"

# Streamlit app
st.title("Folium Map with GeoJSON Data")

# Create a Folium map
m = folium.Map(location=[39.5, -98.35], zoom_start=4)

# Add each GeoJSON file to the map
for file_name in geojson_files:
    geojson_url = get_raw_github_url(repo_url, file_name)
    response = requests.get(geojson_url)
    if response.status_code == 200:
        geojson_data = response.json()
        GeoJson(geojson_data, name=file_name).add_to(m)
    else:
        st.error(f"Failed to load {file_name}")

# Display the map in Streamlit
st_folium(m, width=700, height=500)
