from collections import defaultdict
import matplotlib
from matplotlib import cm
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pylab as plt
from random import randint, random
import cPickle
from datetime import datetime


HIT, STICK = 1, 0


def action_value_to_value_function(action_value_function):
    value_function = defaultdict(float)
    keys = action_value_function.keys()

    for key in keys:
        dealer, player, action = key
        hit_reward = action_value_function[(dealer, player, HIT)]
        stick_reward = action_value_function[(dealer, player, STICK)]
        value_function[(dealer, player)] = max(hit_reward, stick_reward)

    return value_function


# if our random value > epsilon, then pick HIT or STICK, depending on which action is better (exploitation)
# else randomly return HIT or STICK (exploration)
def epsilon_greedy_policy(action_value_function, state, epsilon, features=None):
    if random() > epsilon:
        hit_value, stick_value = 0, 0
        if features is None:
            hit_value = action_value_function[(state.dealer, state.player, HIT)]
            stick_value = action_value_function[(state.dealer, state.player, STICK)]
        else:
            hit_value = action_value_function[(tuple(features), HIT)]
            stick_value = action_value_function[(tuple(features), STICK)]

        if hit_value > stick_value:
            return HIT
        elif hit_value < stick_value:
            return STICK
        else:
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
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
    fname = title+str(datetime.now())+".png"
    print "Saving", fname
    plt.savefig(fname)
    # plt.show()


def save(data, file):
    fo = open(file, 'w')
    cPickle.dump(data, fo, protocol=2)
    fo.close()


def load(file):
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict


