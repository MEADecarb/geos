import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import requests
from typing import Dict, Any

@st.cache_data
def load_geojson(url: str) -> gpd.GeoDataFrame:
    return gpd.read_file(url)

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

@st.cache_data
def fetch_arcgis_data(url: str) -> Dict[str, Any]:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def add_arcgis_layer(map_obj: folium.Map, arcgis_data: Dict[str, Any]) -> None:
    arcgis_layer = folium.FeatureGroup(name='ArcGIS Layer')
    folium.GeoJson(arcgis_data).add_to(arcgis_layer)
    arcgis_layer.add_to(map_obj)

def create_map(geojson_data: gpd.GeoDataFrame, arcgis_data: Dict[str, Any]) -> folium.Map:
    m = folium.Map(
        location=[geojson_data.geometry.centroid.y.mean(), geojson_data.geometry.centroid.x.mean()],
        zoom_start=10
    )
    folium.GeoJson(geojson_data).add_to(m)
    add_arcgis_layer(m, arcgis_data)
    folium.LayerControl().add_to(m)
    return m

def main():
    st.set_page_config(page_title="Interactive Map with Table", layout="wide")
    
    # URLs of your GeoJSON and CSV files on GitHub
    geojson_url = 'https://raw.githubusercontent.com/yourusername/yourrepo/main/yourfile.geojson'
    data_url = 'https://raw.githubusercontent.com/yourusername/yourrepo/main/yourfile.csv'
    arcgis_url = 'https://services.arcgis.com/njFNhDsUCentVYJW/ArcGIS/rest/services/Enough_Act_School_Locations/FeatureServer/137?f=pjson'

    st.title("Interactive Map with Table")

    # Load data
    with st.spinner("Loading data..."):
        geojson_data = load_geojson(geojson_url)
        data = load_data(data_url)
        arcgis_data = fetch_arcgis_data(arcgis_url)

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Map")
        map_folium = create_map(geojson_data, arcgis_data)
        folium_static(map_folium, width=700, height=500)

    with col2:
        st.subheader("Data Table")
        st.dataframe(data, height=500)

    # Expandable sections for raw data
    with st.expander("Show GeoJSON Data"):
        st.write(geojson_data)

    with st.expander("Show CSV Data"):
        st.write(data)

if __name__ == "__main__":
    main()
