from collections import defaultdict
from random import randint, random
from state import State
from env import step
from common import epsilon_greedy_policy, plot_value_function, action_value_to_value_function, load
from progressbar import ProgressBar
import pylab as plt
from mc_control import monte_carlo_control


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


def sarsa(gamma):
    n_episodes = 1000
    epi_batch = 100
    episodes = xrange(n_episodes)
    action_value_function = defaultdict(float)
    n_zero = 100
    n_states = defaultdict(int)
    n_state_actions = defaultdict(int)

    if gamma == 0.0 or gamma == 1.0:
        mses = []

    for episode in episodes:
        if episode%epi_batch == 0:
            if gamma == 0.0 or gamma == 1.0:
                mses.append(compute_mse(action_value_function))

        # initialize state, action, epsilon, and eligibility-trace
        state = State()
        current_dealer = state.dealer
        current_player = state.player

        epsilon = float(n_zero) / (n_zero + n_states[(current_dealer, current_player)])
        current_action = epsilon_greedy_policy(action_value_function, state, epsilon)
        eligibility = defaultdict(int)

        while not state.terminal:
            n_states[(current_dealer, current_player)] += 1
            n_state_actions[(current_dealer, current_player, current_action)] += 1

            reward = step(state, current_action)
            new_dealer = state.dealer
            new_player = state.player

            epsilon = float(n_zero) / (n_zero + n_states[(new_dealer, new_player)])

            new_action = epsilon_greedy_policy(action_value_function, state, epsilon)

            alpha = 1.0 / n_state_actions[(current_dealer, current_player, current_action)]
            prev_action_value = action_value_function[(current_dealer, current_player, current_action)]
            new_action_value = action_value_function[(new_dealer, new_player, new_action)]

            delta = reward + new_action_value - prev_action_value
            eligibility[(current_dealer, current_player, current_action)] += 1

            for key in action_value_function.keys():
                dealer, player, action = key

                # update the action value function
                action_value_function[(dealer, player, action)] \
                    += alpha * delta * eligibility[(dealer, player, action)]

                # update eligibility-trace
                eligibility[(dealer, player, action)] *= gamma

            # update state and action
            current_dealer = new_dealer
            current_player = new_player
            current_action = new_action


    if gamma == 0.0 or gamma == 1.0:
        mses.append(compute_mse(action_value_function))

    # plot mses curve
    if gamma == 0.0 or gamma == 1.0:
        x = range(0, n_episodes + 1, epi_batch)
        fig = plt.figure()
        plt.title('Learning curve of Mean-Squared Error against episode number: gamma = ' + str(gamma))
        plt.xlabel("episode number")
        plt.xlim([0, n_episodes])
        plt.xticks(range(0, n_episodes + 1, epi_batch))
        plt.ylabel("Mean-Squared Error")
        plt.plot(x, mses)
        plt.show()

    mse = compute_mse(action_value_function)

    return mse

if __name__ == '__main__':
    mses = [0 for i in range(11)]

    pbar = ProgressBar(maxval=11).start()
    for i in range(11):
        mses[i] = sarsa(gamma=float(i) / 10)
        pbar.update(i)

    pbar.finish()

    # plot the mse against gamma
    x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    fig = plt.figure()
    plt.title('Mean-Squared Error against gamma')
    plt.xlabel("gamma")
    plt.xlim([0., 1.])
    plt.xticks(x)
    plt.ylabel("Mean-Squared Error")
    plt.plot(x, mses)
    plt.show()

