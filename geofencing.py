import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt

# https://towardsdatascience.com/the-art-of-geofencing-in-python-e6cc237e172d

df = pd.read_csv(r"C:\Users\HP\PycharmProjects\playground\go-track-trackPoints.csv")
print(df.head())

px.set_mapbox_access_token(r'pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w')
px.scatter_mapbox(gdf, lat='latitude', lon='longitude', size_max=6, zoom=8, width=1200, height=800)
