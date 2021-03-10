import pandas as pd
import geopandas as gpd
import math
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

# Create a map
m = folium.Map(location=[42.32, -71.0589], tiles='openstreetmap', zoom_start=10)

area_data = pd.read_csv('ny_bay_AIS_2020_01_01.csv')


Marker([42.32, -71.0589]).add_to(m)



# Display the map
m.save('yesss.html')







#try to use .isin() to arrange data in pandas
#try to use pandas for your csv data
