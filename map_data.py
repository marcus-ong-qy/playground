import datetime
import csv


class Node:  # point in map representing vessel location at a certain time
    def __init__(self, mmsi, pos, time, name):
        self.mmsi = mmsi
        self.pos = pos
        self.time = time
        self.name = name


def gen_area_data(csv_file_path, box_range, time_start, time_end):
    area_data = {}  # Dict with mmsi(string) as key and a list of Node objects as value

    with open(csv_file_path, mode='r') as file:  # ny bay area
        csv_file = csv.reader(file)
        next(csv_file)

        for line in csv_file:

            time = datetime.datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%S')

            if box_range[2] < float(line[2]) < box_range[3] and box_range[0] < float(line[3]) < box_range[1] and \
                    time_start <= time <= time_end:

                mmsi = str(line[0])
                pos = (float(line[2]), float(line[3]))
                name = line[7]
                if mmsi not in area_data.keys():
                    area_data[mmsi] = [Node(mmsi, pos, time, name)]

                else:
                    area_data[mmsi].append(Node(mmsi, pos, time, name))

    return area_data
