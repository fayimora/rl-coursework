from collections import defaultdict
from common import load, epsilon_greedy_policy
from linear_function import LinearFunction
import numpy as np
from state import State
from env import step
from progressbar import ProgressBar
import matplotlib
import pylab as plt
matplotlib.use('Agg')
from datetime import datetime


HIT, STICK = 1, 0


def calculate_mse(action_value_function):
    mc_action_value_function = load('mc_result.dat')
    linear_function = LinearFunction()
    mse, count = 0, 0

    for dealer in range(1, 11):
        for player in range(1, 22):
            for action in range(0, 2):
                state = State(dealer=dealer, player=player)
                linear_function.update(state)
                features = linear_function.get_features()

                mc_reward = mc_action_value_function[(dealer, player, action)]
                reward = action_value_function[(tuple(features), action)]
                mse += (reward - mc_reward) ** 2
                count += 1

    mse /= count
    return mse


def update_action_value_function(action_value_function, (features, action), params):
    features = np.array(features)
    new_value = features.dot(params)
    action_value_function[(tuple(features), action)] = new_value


def sarsa(lambd):
    n_episodes = 1000
    epi_batch = 100
    episodes = xrange(n_episodes)
    action_value_function = defaultdict(float)
    linear_function = LinearFunction()
    params_hit = np.array([0 for i in range(18)])
    params_stick = np.array([0 for i in range(18)])
    n_zero = 10
    epsilon = 0.1
    alpha = 0.01

    if lambd == 0.0 or lambd == 1.0:
        mses = []

    for episode in episodes:
        if episode%epi_batch == 0:
            if lambd == 0.0 or lambd == 1.0:
                mses.append(calculate_mse(action_value_function))

        # initialize state, action, epsilon, and eligibility-trace
        state = State()
        linear_function.update(state)
        current_feats = linear_function.get_features()
        action = epsilon_greedy_policy(action_value_function, state, epsilon, current_feats)
        eligibility_hit = np.array([0 for i in range(18)])
        eligibility_stick = np.array([0 for i in range(18)])

        while not state.terminal:
            np_feats = np.array(current_feats)
            if action is HIT:
                eligibility_hit = np.add(eligibility_hit, np_feats)
            else:
                eligibility_stick = np.add(eligibility_stick, np_feats)

            reward = step(state, action)
            linear_function.update(state)
            new_features = linear_function.get_features()

            # update delta
            delta_hit = reward - np.array(tuple(new_features)).dot(params_hit)
            delta_stick = reward - np.array(tuple(new_features)).dot(params_stick)

            # update Action Value Function
            if action == HIT:
                update_action_value_function(action_value_function, (new_features, action), params_hit)
            else:
                update_action_value_function(action_value_function, (new_features, action), params_stick)

            # update delta, parameters, and eligibility-trace
            if action == HIT:
                delta_hit += action_value_function[(tuple(new_features), HIT)]
            else:
                delta_stick += action_value_function[(tuple(new_features), STICK)]

            params_hit = np.add(params_hit, alpha * delta_hit * eligibility_hit)
            params_stick = np.add(params_stick, alpha * delta_stick * eligibility_stick)
            eligibility_hit = eligibility_hit * lambd
            eligibility_stick = eligibility_stick * lambd

            # decide an action
            action = epsilon_greedy_policy(action_value_function, state, epsilon, new_features)

            # update state and action
            current_features = new_features


    if lambd == 0.0 or lambd == 1.0:
        mses.append(calculate_mse(action_value_function))

    # plot mses curve
    if lambd == 0.0 or lambd == 1.0:
        print "Plotting learning curve for $\lambda$=",lambd
        x = range(0, n_episodes + 1, epi_batch)
        fig = plt.figure()
        plt.title('Learning curve of MSE against Episodes @ $\lambda$ = ' + str(lambd))
        plt.xlabel("episode number")
        plt.xlim([0, n_episodes])
        plt.xticks(range(0, n_episodes + 1, epi_batch))
        plt.ylabel("Mean-Squared Error (MSE)")
        plt.plot(x, mses)
        fname = "lapprox_mse_lambda%f_%s.png" % (lambd, str(datetime.now()))
        plt.savefig(fname)
        # plt.show()

    mse = calculate_mse(action_value_function)

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
    fname = "lapprox_mse_vs_lamnda_" + str(datetime.now())+".png"
    plt.savefig(fname)
    # plt.show()




