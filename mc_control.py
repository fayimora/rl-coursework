from state import State
from env import step
from value_functions import ActionValue
from collections import defaultdict
from random import randint, random
from common import action_value_to_value_function, plot_value_function
from progressbar import ProgressBar

HIT, STICK = 1, 0

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



if __name__ == '__main__':
    action_value_function = defaultdict(float)
    n_states = defaultdict(int)
    n_state_actions = defaultdict(int)

    n_zero = 100
    episodes = xrange(1000000)

    pbar = ProgressBar(maxval=len(episodes)).start()
    for episode in episodes:
        state = State()
        while not state.terminal:
            player = state.player
            dealer = state.dealer

            epsilon = float(n_zero) / (n_zero + n_states[(dealer, player)])
            action = epsilon_greedy_policy(action_value_function, state, epsilon)

            n_states[(dealer, player)] += 1
            n_state_actions[(dealer, player, action)] += 1

            reward = step(state, action)

            # update the action value function
            alpha = 1.0 / n_state_actions[(dealer, player, action)]
            action_value = action_value_function[(dealer, player, action)]
            action_value_function[(dealer, player, action)] += alpha * (reward - action_value)

        pbar.update(episode)
    pbar.finish()
    value_function = action_value_to_value_function(action_value_function)
    plot_value_function(value_function, "Optimal Value Function: Question 2")


