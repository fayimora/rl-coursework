from state import State
from env import step
from collections import defaultdict
from random import randint, random
from common import action_value_to_value_function, plot_value_function, epsilon_greedy_policy, save
from progressbar import ProgressBar


def monte_carlo_control():
    action_value_function = defaultdict(float)
    n_s = defaultdict(int)
    n_s_a = defaultdict(int)

    n_zero = 1E5
    episodes = xrange(int(1E8))

    pbar = ProgressBar(maxval=len(episodes)).start()
    for episode in episodes:
        state = State()
        while not state.terminal:
            player = state.player
            dealer = state.dealer

            epsilon = float(n_zero) / (n_zero + n_s[(dealer, player)])
            action = epsilon_greedy_policy(action_value_function, state, epsilon)

            n_s[(dealer, player)] += 1
            n_s_a[(dealer, player, action)] += 1

            reward = step(state, action)

            # update the action value function
            alpha = 1.0 / n_s_a[(dealer, player, action)]
            new_reward = action_value_function[(dealer, player, action)]
            action_value_function[(dealer, player, action)] += alpha * (reward - new_reward)

        pbar.update(episode)
    pbar.finish()
    value_function = action_value_to_value_function(action_value_function)
    plot_value_function(value_function, "Optimal Value Function: Question 2")

    return action_value_function


if __name__ == '__main__':
    mc_action_value_function = monte_carlo_control()
    save(mc_action_value_function, "mc_result.dat")
