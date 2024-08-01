import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import requests
from typing import Dict, Any
import urllib.request
import urllib.error

@st.cache_data
def load_geojson(url: str) -> gpd.GeoDataFrame:
  try:
      with urllib.request.urlopen(url) as response:
          return gpd.read_file(response)
  except urllib.error.HTTPError as e:
      st.error(f"HTTP Error {e.code}: Unable to access the GeoJSON file. Please check the URL and try again.")
      st.stop()
  except urllib.error.URLError as e:
      st.error(f"URL Error: {e.reason}. Please check your internet connection and the URL.")
      st.stop()
  except Exception as e:
      st.error(f"An unexpected error occurred: {str(e)}")
      st.stop()

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
  try:
      return pd.read_csv(url)
  except Exception as e:
      st.error(f"Error loading CSV data: {str(e)}")
      st.stop()

@st.cache_data
def fetch_arcgis_data(url: str) -> Dict[str, Any]:
  try:
      response = requests.get(url)
      response.raise_for_status()
      return response.json()
  except requests.RequestException as e:
      st.error(f"Error fetching ArcGIS data: {str(e)}")
      st.stop()

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
  geojson_url = 'https://github.com/MEADecarb/schools/blob/main/MDHB550CensusTracts.geojson'
  arcgis_url = 'https://services.arcgis.com/njFNhDsUCentVYJW/ArcGIS/rest/services/Enough_Act_School_Locations/FeatureServer/137?f=pjson'

  st.title("Interactive Map with Table")

  # Load data
  with st.spinner("Loading data..."):
      try:
          geojson_data = load_geojson(geojson_url)
          data = load_data(data_url)
          arcgis_data = fetch_arcgis_data(arcgis_url)
      except Exception as e:
          st.error(f"An error occurred while loading data: {str(e)}")
          st.stop()

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
