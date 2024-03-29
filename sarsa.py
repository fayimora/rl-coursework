from collections import defaultdict
from random import randint, random
from state import State
from env import step
from common import epsilon_greedy_policy, plot_value_function, action_value_to_value_function, load
from progressbar import ProgressBar
import matplotlib
import pylab as plt
matplotlib.use('Agg')
from mc_control import monte_carlo_control
from datetime import datetime


def compute_mse(action_value_function):
    mc_action_value_function = load('mc_result.dat')
    err_sq, count = 0, 0
    for dealer in xrange(1, 11):
        for player in xrange(1, 22):
            for action in xrange(0, 2):
                v1 = action_value_function[(dealer, player, action)]
                v2 = mc_action_value_function[(dealer, player, action)]
                err_sq += (v1 - v2) ** 2
                count += 1

    mse = err_sq / count
    return mse


def sarsa(lambd):
    n_episodes = 1000
    epi_batch = 100
    episodes = xrange(n_episodes)
    action_value_function = defaultdict(float)
    n_zero = 100
    n_s = defaultdict(int)
    n_s_a = defaultdict(int)

    if lambd == 0.0 or lambd == 1.0:
        mses = []

    for episode in episodes:
        if episode%epi_batch == 0:
            if lambd == 0.0 or lambd == 1.0:
                mses.append(compute_mse(action_value_function))

        # initialize state, action, epsilon, and eligibility-trace
        state = State()
        current_dealer = state.dealer
        current_player = state.player

        epsilon = float(n_zero) / (n_zero + n_s[(current_dealer, current_player)])
        current_action = epsilon_greedy_policy(action_value_function, state, epsilon)
        eligibility_trace = defaultdict(int)

        while not state.terminal:
            n_s[(current_dealer, current_player)] += 1
            n_s_a[(current_dealer, current_player, current_action)] += 1

            reward = step(state, current_action)
            new_dealer = state.dealer
            new_player = state.player

            epsilon = float(n_zero) / (n_zero + n_s[(new_dealer, new_player)])

            new_action = epsilon_greedy_policy(action_value_function, state, epsilon)

            alpha = 1.0 / n_s_a[(current_dealer, current_player, current_action)]
            prev_action_value = action_value_function[(current_dealer, current_player, current_action)]
            new_action_value = action_value_function[(new_dealer, new_player, new_action)]

            delta = reward + new_action_value - prev_action_value
            eligibility_trace[(current_dealer, current_player, current_action)] += 1

            for key in action_value_function.keys():
                dealer, player, action = key

                # update the action value function
                action_value_function[(dealer, player, action)] \
                    += alpha * delta * eligibility_trace[(dealer, player, action)]

                # update eligibility-trace
                eligibility_trace[(dealer, player, action)] *= lambd

            # update state and action
            current_dealer = new_dealer
            current_player = new_player
            current_action = new_action


    if lambd == 0.0 or lambd == 1.0:
        mses.append(compute_mse(action_value_function))

    # plot mses curve
    if lambd == 0.0 or lambd == 1.0:
        print "Plotting learning curve for $\lambda$=",lambd
        x = range(0, n_episodes + 1, epi_batch)
        fig = plt.figure()
        plt.title('Learning curve of MSE against episode number: $\lambda$ = ' + str(lambd))
        plt.xlabel("episode number")
        plt.xlim([0, n_episodes])
        plt.xticks(range(0, n_episodes + 1, epi_batch))
        plt.ylabel("Mean-Squared Error (MSE)")
        plt.plot(x, mses)
        fname = "mse_lambda%f_%s.png" % (lambd, str(datetime.now()))
        plt.savefig(fname)
        # plt.show()

    mse = compute_mse(action_value_function)

    return mse

if __name__ == '__main__':
    mses = [0 for i in range(11)]

    pbar = ProgressBar(maxval=len(mses)).start()
    for i in range(11):
        mses[i] = sarsa(lambd=float(i) / 10)
        pbar.update(i)

    pbar.finish()

    # plot the mse against lambda
    x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    fig = plt.figure()
    plt.title('Mean-Squared Error against $\lambda$')
    plt.xlabel("$\lambda$")
    plt.xlim([0., 1.])
    plt.xticks(x)
    plt.ylabel("Mean-Squared Error")
    plt.plot(x, mses)
    fname = "mse_vs_lamnda_" + str(datetime.now())+".png"
    plt.savefig(fname)
    # plt.show()

