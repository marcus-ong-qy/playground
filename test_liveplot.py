import datetime
import matplotlib.pyplot as plt
import random
from map_data import gen_area_data
from matplotlib.animation import FuncAnimation


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


def animate(i, xlist, ylist, vessel_path_list):  # each i is 1 frame

    xlist.append(vessel_path_list[i].pos[1])
    ylist.append(vessel_path_list[i].pos[0])
    plt.cla()  # clears plots
    plt.plot(xlist, ylist)

def plot_trail(mmsi, data):  # plots live trail of one vessel

    vessel_nodes_list = data[mmsi]

    vessel_path_list = sort_node(vessel_nodes_list)
    return vessel_path_list




def main():
    BBox = (-74.35, -73.71, 40.38, 40.66)  # lonmin, lonmax, latmin, latmax

    start_time_input = '2020-01-01T00:00:00'
    end_time_input = '2020-01-01T23:59:59'

    start_time = datetime.datetime.strptime(start_time_input, '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.datetime.strptime(end_time_input, '%Y-%m-%dT%H:%M:%S')

    csv_data = 'ny_bay_AIS_2020_01_01.csv'
    img = 'ny_bay (-74.35, -73.71, 40.38, 40.66).png'

    area_data = gen_area_data(csv_data, BBox, start_time, end_time)

    mmsi = '367518920'

    vessel_path_list = plot_trail(mmsi, area_data)

    im = plt.imread(img)
    fig, ax = plt.subplots()

    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.imshow(im, zorder=0, extent=BBox, aspect='equal')

    xlist = []
    ylist = []
    ani = FuncAnimation(fig, animate, fargs=(xlist, ylist, vessel_path_list),
                        frames=len(vessel_path_list), interval=100)
    plt.show()


if __name__ == '__main__':
    main()
