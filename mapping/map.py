import streamlit as st
import geopandas as gpd
import urllib.request
import urllib.error
import json

@st.cache_data
def load_geojson(url: str) -> gpd.GeoDataFrame:
  try:
      with urllib.request.urlopen(url) as response:
          content = response.read().decode('utf-8')
          # Parse the JSON content
          geojson_dict = json.loads(content)
          # Create GeoDataFrame from the parsed GeoJSON
          return gpd.GeoDataFrame.from_features(geojson_dict["features"])
  except urllib.error.HTTPError as e:
      st.error(f"HTTP Error {e.code}: Unable to access the GeoJSON file. Please check the URL and try again.")
      st.stop()
  except urllib.error.URLError as e:
      st.error(f"URL Error: {e.reason}. Please check your internet connection and the URL.")
      st.stop()
  except json.JSONDecodeError:
      st.error("The file at the provided URL is not a valid JSON.")
      st.stop()
  except KeyError:
      st.error("The JSON file does not have the expected 'features' key.")
      st.stop()
  except Exception as e:
      st.error(f"An unexpected error occurred while loading GeoJSON: {str(e)}")
      st.stop()
