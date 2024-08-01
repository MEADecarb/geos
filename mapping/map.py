import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import requests

@st.cache
def load_geojson(url):
    return gpd.read_file(url)

@st.cache
def load_data(url):
    return pd.read_csv(url)

def add_arcgis_layer(map_obj, arcgis_url):
    arcgis_layer = folium.FeatureGroup(name='ArcGIS Layer')
    folium.GeoJson(arcgis_url).add_to(arcgis_layer)
    arcgis_layer.add_to(map_obj)

def create_map(geojson_data, arcgis_url):
    m = folium.Map(location=[geojson_data.geometry.centroid.y.mean(), geojson_data.geometry.centroid.x.mean()], zoom_start=10)
    folium.GeoJson(geojson_data).add_to(m)
    add_arcgis_layer(m, arcgis_url)
    folium.LayerControl().add_to(m)
    return m

# URLs of your GeoJSON and CSV files on GitHub
geojson_url = 'https://github.com/MEADecarb/schools/blob/main/MDHB550CensusTracts.geojson'
arcgis_url = 'https://services.arcgis.com/njFNhDsUCentVYJW/ArcGIS/rest/services/Enough_Act_School_Locations/FeatureServer/137?f=pjson'

st.title("Interactive Map with Table")

# Load data
geojson_data = load_geojson(geojson_url)
data = load_data(data_url)

# Display map
st.subheader("Map")
map_folium = create_map(geojson_data, arcgis_url)
st_folium(map_folium, width=700, height=500)

# Display table
st.subheader("Data Table")
st.dataframe(data)

if st.checkbox('Show GeoJSON Data'):
    st.write(geojson_data)

if st.checkbox('Show CSV Data'):
    st.write(data)
