from random import randint

class State:
    # initialise the state of the player and dealer
    def __init__(self, dealer=None, player=None):
        if dealer is not None and player is not None:
            self.dealer = dealer
            self.player = player
        elif dealer is None and player is None:
            self.dealer = randint(1, 10)
            self.player = randint(1, 10)

