# python_live_plot.py

import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_values = []
y_values = []

index = count()
base = 100
y = base


def animate(i):
    global y
    x_values.append(next(index))
    y_values.append(y)
    perc = 1 + random.randint(-100, 105)/1000
    y *= perc if perc != 0 else None
    plt.cla()  # clears plots
    plt.plot(x_values, y_values)


ani = FuncAnimation(plt.gcf(), animate, 1000)

plt.tight_layout()
plt.show()
