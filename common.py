from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pylab


HIT, STICK = 1, 0

def action_value_to_value_function(action_value_function):
    value_function = defaultdict(float)
    keys = action_value_function.keys()

    for key in keys:
        dealer, player, action = key[0], key[1], key[2]
        hit_reward = action_value_function.get((dealer, player, HIT))
        stick_reward = action_value_function.get((dealer, player, STICK))

        if hit_reward > stick_reward:
            value_function[(dealer, player)] = hit_reward
        else:
            value_function[(dealer, player)] = stick_reward

    return value_function


def plot_value_function(value_function, title):
    # plot the value function where x isthe dealer and y is the player
    x = range(1, 11)
    y = range(1, 22)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[0. for i in range(len(x))] for j in range(len(y))])
    for i in x:
        for j in y:
            Z[j - 1][i - 1] = value_function[(i, j)]

    # fig = pylab.figure()
    ax = Axes3D(pylab.figure())
    pylab.title(title)
    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1)
    pylab.show()


