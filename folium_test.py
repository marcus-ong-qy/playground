import pandas as pd
# import geopandas as gpd
import math
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

# Create a map
m = folium.Map(location=[40.721, -73.8635],
               tiles='http://localhost:3650/api/tiles/2017-07-03_new-york_new-york/{z}/{x}/{y}.png',
               zoom_start=10, attr='Maps powered by OpenStreetMap data')

area_data = pd.read_csv('ny_bay_AIS_2020_01_01.csv')


Marker([40.721, -73.8635]).add_to(m)

# Display the map
m.save('yes.html')







#try to use .isin() to arrange data in pandas
#try to use pandas for your csv data
