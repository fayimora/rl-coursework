from state import State
from env import step
from value_functions import ActionValue
from collections import defaultdict
from random import randint, random

# stub epsilon for now
def epsilon_greedy(action_value, state, epsilon):
    HIT = 0
    STICK = 1
    if randint(1, 10) > 6:
        return HIT
    else:
        return STICK


def plot_value_function(value_function, title):
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import pylab

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


if __name__ == '__main__':
    action_value_function = ActionValue(float)
    n_states = defaultdict(int)
    n_state_actions = defaultdict(int)

    n_zero = 100
    episodes = xrange(100000)

    for episode in episodes:
        state = State()
        while not state.terminal:
            player = state.player
            dealer = state.dealer

            epsilon = float(n_zero) / (n_zero + n_states[(dealer, player)])
            action = epsilon_greedy(action_value_function, state, epsilon)

            n_states[(dealer, player)] += 1
            n_state_actions[(dealer, player, action)] += 1

            reward = step(state, action)

            # update the action value function
            alpha = 1.0 / n_state_actions[(dealer, player, action)]
            action_value = action_value_function[(dealer, player, action)]
            action_value_function[(dealer, player, action)] += alpha * (reward - action_value)

    value_function = action_value_function.to_value_function()
    plot_value_function(value_function, "Optimal Value Function: Question 2")

