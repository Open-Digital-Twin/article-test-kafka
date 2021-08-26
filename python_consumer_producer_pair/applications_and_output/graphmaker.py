import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sys import argv, exit

loose_scales = False

if len(argv) == 2:
    loose_scales = argv[1]
if len(argv) > 2:
    exit('too many arguments')


x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('output_consumer', skiprows=5, usecols=[1], names=['delay'])
    x = data.index
    y1 = data['delay'] * 1000
    message_mean = y1.mean()
    plt.cla()
    plt.plot(x, y1, label=f'mean delay per message: {message_mean.round(10)}')
    plt.ylabel('delay (mili-seconds)')
    plt.xlabel('number of measurements')
    plt.legend(loc='upper left')
    if not loose_scales:
        plt.ylim([0, 160])
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()