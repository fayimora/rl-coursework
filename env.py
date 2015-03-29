from random import randint, random

# make the hit and stack actions numbers so my if statements are cleaner
HIT = 1
STICK = 0


def draw_card():
    def draw_black():
        return randint(1, 10)

    def draw_red():
        return -randint(1, 10)

    """black is drwan with probability 2/3"""
    probability = random()
    if probability <= 2/3.0:
        return draw_black()
    else:
        return draw_red()


def is_burst(score):
    return score > 21 or score < 1


def step(state, action):
    player_is_burst = False
    dealer_is_burst = False

    if action is HIT:
        state.player += draw_card()
        player_is_burst = is_burst(state.player)

        if player_is_burst:
                state.terminal = True
    elif action is STICK:
        dealer_action = HIT
        # dealer's turn to play since player has given up
        while dealer_action == HIT and not dealer_is_burst:
            state.dealer += draw_card()
            dealer_is_burst = is_burst(state.dealer)
            # STICK if > 17 else HIT
            dealer_action = HIT if 1 <= state.dealer <= 16 else STICK

        state.terminal = True


    # if the player has gone burst, reward = -1
    # if the dealer has gone burst, reward = 1
    # if the player has a larger score, it wins(reward=1) otherwise it looses(reward=0)
    # a draw gives reward = 0

    # Only compute reward if we are in a terminal state
    reward = 0
    if state.terminal:
        if player_is_burst:
            reward = -1
        elif dealer_is_burst:
            reward = 1
        else:
            if state.player > state.dealer:
                reward = 1
            elif state.player < state.dealer:
                reward = -1
            elif state.player == state.dealer: # a draw
                reward = 0

    else:
        reward = 0

    return reward


