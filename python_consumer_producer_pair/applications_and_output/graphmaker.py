import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('output_consumer')
    x = data['x_value']
    y1 = data['delay']
    message_mean = y1.mean()

    plt.cla()
    plt.plot(x, y1, label=f'mean delay per message: {message_mean.round(10)}')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()