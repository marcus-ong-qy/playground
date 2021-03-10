import datetime
import matplotlib.pyplot as plt
import csv
import random
import folium
from folium import Choropleth, Circle, Marker


class Node:  # point in map representing vessel location at a certain time
    def __init__(self, mmsi, pos, time, name):
        self.mmsi = mmsi
        self.pos = pos
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

                mmsi = line[0]
                pos = (float(line[2]), float(line[3]))  # lat, lon
                name = line[7]
                if mmsi not in area_data.keys():
                    area_data[mmsi] = [Node(mmsi, pos, time, name)]

                else:
                    area_data[mmsi].append(Node(mmsi, pos, time, name))

    return area_data


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


def plot_trail(data, box_range):  # plots trails of vessels within a time range

    m = folium.Map(location=[(box_range[3] + box_range[2]) / 2, (box_range[1] + box_range[0]) / 2],
                   tiles='openstreetmap', zoom_start=10)

    color_list = ['red', 'green', 'blue']
    icon_url = 'boat.png'

    for vessel_nodes_list in data.values():
        x = []
        y = []
        vessel_path_list = sort_node(vessel_nodes_list)
        for ts in vessel_path_list:
            icon = folium.features.CustomIcon(icon_url, icon_size=(8, 8))
            Marker([ts.pos[0], ts.pos[1]], icon=icon, popup=ts.name).add_to(m)

    m.save('test.html')


def main():
    BBox = (-74.35, -73.71, 40.38, 40.66)  # lonmin, lonmax, latmin, latmax

    start_time_input = '2020-01-01T00:00:00'
    end_time_input = '2020-01-01T01:00:00'

    start_time = datetime.datetime.strptime(start_time_input, '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.datetime.strptime(end_time_input, '%Y-%m-%dT%H:%M:%S')

    csv_data = 'ny_bay_AIS_2020_01_01.csv'

    area_data = gen_area_data(csv_data, BBox, start_time, end_time)
    plot_trail(area_data, BBox)


if __name__ == '__main__':
    main()
