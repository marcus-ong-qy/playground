import datetime
import matplotlib.pyplot as plt
import csv
import random
import folium
from folium import Choropleth, Circle, Marker
import plotly.graph_objects as go
import numpy as np
import math

'''
PLAN:
 fig.data contains 1 frame per second, followed by line plots

'''


class Node:  # point in map representing vessel location at a certain time
    def __init__(self, mmsi, pos, time, name):
        self.mmsi = mmsi
        self.pos = pos # lat, lon (y, x)
        self.time = time
        self.name = name


def gen_area_data(csv_file_path, box_range, time_start, time_end):
    area_data = {}  # Dict with mmsi as key and a list of Node objects as value

    with open(csv_file_path, mode='r') as file:  # ny bay area
        csv_file = csv.reader(file)
        next(csv_file)

        for line in csv_file:

            time = datetime.datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%S')

            if box_range[2] < float(line[2]) < box_range[3] and box_range[0] < float(line[3]) < box_range[1] and \
                    time_start <= time <= time_end:

                mmsi = str(line[0])
                pos = (float(line[2]), float(line[3]))  # lat, lon
                name = line[7]
                if mmsi not in area_data.keys():
                    area_data[mmsi] = [Node(mmsi, pos, time, name)]

                else:
                    area_data[mmsi].append(Node(mmsi, pos, time, name))

    return area_data  # Dict with mmsi as key and a list of Node objects as value
# Returns area_data: Dict with mmsi(str) as key and a list of Node objects as value


def gen_fig():
    global xm, xM, ym, yM, vessel_name, vessel_mmsi, start_time, end_time
    # fig data

    # fig layout
    layout_xaxis = dict(range=[xm, xM], autorange=False, zeroline=False)
    layout_yaxis = dict(range=[ym, yM], autorange=False, zeroline=False)


    # Create figure
    fig = go.Figure(
        layout=go.Layout(
            xaxis=layout_xaxis,
            yaxis=layout_yaxis,
            title_text="Track History of {} (mmsi:{}) from {} to {}"
                .format(vessel_name, vessel_mmsi, start_time, end_time),
            hovermode="closest",
        ),
    )

    return fig


def sort_node(node_list):  # early to late
    # input list of unsorted nodes and sort them in chronological order

    def swap(i, j):
        node_list[i], node_list[j] = node_list[j], node_list[i]

    n = len(node_list)
    swapped = True

    x = -1
    while swapped:
        swapped = False
        x = x + 1
        for i in range(1, n - x):
            if node_list[i - 1].time > node_list[i].time:
                swap(i - 1, i)
                swapped = True

    return node_list
# input list of unsorted nodes and sort them in chronological order
# Returns node_list, a list of sorted nodes


# Generate curve data

def plot_trace(vessel_path_list):
    tf_count = 0

    for node in vessel_path_list:  # generate traces for animated point
        x_step = (node.pos[1],)
        y_step = (node.pos[0],)
        fig.add_trace(
            go.Scatter(
                visible=False,
                mode="markers",
                name=node.name + ' @' + str(node.time),
                marker=dict(color="red", size=10),
                x=x_step,
                y=y_step
            )
        )
        tf_count += 1

    fig.data[-1].visible = True  # set default plot to visible

    return tf_count


def plot_line(vessel_name, x, y):
    fig.add_trace(  # add line plot
        go.Scatter(
            mode="lines",
            name=vessel_name,
            visible=True,
            marker=dict(color="blue"),
            x=x,
            y=y
        )
    )


def gen_slider(fig, tf_count):
    # set slider steps
    steps = []

    for i in range(tf_count):  # set point to visible
        step = dict(
            method="update",
            args=[{"visible": ([False] * tf_count) +  # scatter plots' visibility
                              ([True] * (len(fig.data) - tf_count))}],  # set line plots to be always visible
        )
        step["args"][0]["visible"][i] = True  # set scatter plots' visibility

        steps.append(step)

    sliders = [dict(
        active=(tf_count - 1),
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(sliders=sliders)


def latlongdeg_to_xtileytile(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


BBox = (-74.35, -73.71, 40.38, 40.66)  # lonmin, lonmax, latmin, latmax

start_time_input = '2020-01-01T00:00:00'
end_time_input = '2020-01-01T23:00:00'

start_time = datetime.datetime.strptime(start_time_input, '%Y-%m-%dT%H:%M:%S')
end_time = datetime.datetime.strptime(end_time_input, '%Y-%m-%dT%H:%M:%S')

csv_data = 'ny_bay_AIS_2020_01_01.csv'

area_data = gen_area_data(csv_data, BBox, start_time, end_time)
# Dict with mmsi(str) as key and a list of Node objects as value


x = []
y = []
xm = BBox[0]
xM = BBox[1]
ym = BBox[2]
yM = BBox[3]
sample_mmsi = '367518920'


vessel_nodes_list = area_data[sample_mmsi]
vessel_path_list = sort_node(vessel_nodes_list)

vessel_mmsi = vessel_path_list[0].mmsi
vessel_name = vessel_path_list[0].name

for ts in vessel_path_list:
    x.append(ts.pos[1])
    y.append(ts.pos[0])


fig = gen_fig()

tf_count = plot_trace(vessel_path_list)

plot_line(vessel_name, x, y)

gen_slider(fig, tf_count)

# conversion formulae
'''



'''

# wip
def add_img():
    lat_deg = (yM + ym) / 2
    lon_deg = (xM + xm) / 2
    zoom = 9

    xtile, ytile = latlongdeg_to_xtileytile(lat_deg, lon_deg, zoom)

    fig_x = -74.53125  # -180 + (360/2**9)*150
    fig_y = 22.5  # 90 - (180/2**9)*192 this one is wrong tell me why ~40.98 think need use trigo
    sizex = 0.703125  # 360/2**9
    sizey = 0.3515625  # 180/2**9

    fig.add_layout_image(
            dict(
                source="http://localhost:8080/styles/klokantech-basic/9/150/192.png",
                xref="x",
                yref="y",
                x=fig_x,  # top left corner
                y=fig_y,
                sizex=sizex,
                sizey=sizey,
                sizing="stretch",
                opacity=0.5,
                layer="below")
    )

    fig.update_layout(template="plotly_white")


add_img()

fig.show()
