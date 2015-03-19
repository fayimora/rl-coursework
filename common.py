from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pylab as plt
from random import randint, random


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


# if our random value > epsilon, then pick HIT or STICK, depending on which action is better (exploitation)
# else randomly return HIT or STICK (exploration)
def epsilon_greedy_policy(action_value, state, epsilon):
    if random() > epsilon:
        hit_value = action_value[(state.dealer, state.player, HIT)]
        stick_value = action_value[(state.dealer, state.player, STICK)]
        if hit_value > stick_value:
            return HIT
        elif hit_value < stick_value:
            return STICK
        else:
            # return random action when both value functions are same
            if random() > 0.5:
                return HIT
            else:
                return STICK
    else:
        if random() > 0.5:
            return HIT
        else:
            return STICK



def plot_value_function(value_function, title):
    # plot the value function where x isthe dealer and y is the player
    x = range(1, 11)
    y = range(1, 22)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[0. for i in range(len(x))] for j in range(len(y))])
    for i in x:
        for j in y:
            Z[j - 1][i - 1] = value_function[(i, j)]

    fig = plt.figure()
    ax = Axes3D(fig)
    plt.title(title)
    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1)
    plt.show()


