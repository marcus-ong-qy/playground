import datetime
import matplotlib.pyplot as plt
import csv
import random
import folium
from folium import Choropleth, Circle, Marker
import plotly.graph_objects as go
import numpy as np

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

for ts in vessel_path_list:
    x.append(ts.pos[1])
    y.append(ts.pos[0])


# fig data

# fig layout
layout_xaxis = dict(range=[xm, xM], autorange=False, zeroline=False)
layout_yaxis = dict(range=[ym, yM], autorange=False, zeroline=False)


# Create figure
fig = go.Figure(
    layout=go.Layout(
        xaxis=layout_xaxis,
        yaxis=layout_yaxis,
        title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
    ),
)

'''
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
'''

# try to generate a frame every 10min
time_int = datetime.timedelta(minutes=1)
timeframes = []
cur_tf = start_time

while cur_tf < end_time:
    timeframes.append(cur_tf)
    cur_tf += time_int

tf_count = 0

for tf in timeframes:

    s = []
    for node in vessel_path_list:
        if tf <= node.time < tf + time_int:
            # for each 10min tf, plot the latest point
            s.append(node)

    if s:
        t = s[-1]  # choose latest point

        x_step = (t.pos[1],)
        y_step = (t.pos[0],)
        fig.add_trace(
            go.Scatter(
                visible=False,
                mode="markers",
                name=t.name + ' @' + str(t.time),
                marker=dict(color="red", size=10),
                x=x_step,
                y=y_step
            )
        )
        tf_count += 1

    '''elif fig.data:    # check if previous tf have node, if have then plot
        fig.add_trace(fig.data[-1])
        tf_count += 1'''


fig.data[0].visible = True


fig.add_trace(  # line plot
    go.Scatter(
        mode="lines",
        visible=True,
        marker=dict(color="blue"),
        x=x,
        y=y
    )
)


# set slider steps
steps = []

for i in range(tf_count):  # set point to visible
    step = dict(
        method="update",
        args=[{"visible": ([False] * tf_count) +
                          ([True] * (len(fig.data) - tf_count))}],
    )
    step["args"][0]["visible"][i] = True

    steps.append(step)


sliders = [dict(
    active=0,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]


fig.update_layout(
    sliders=sliders
)


fig.show()
