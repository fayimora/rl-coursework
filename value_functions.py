# A value function is simply a map from state -> value
class Value(defaultdict):
    def __getitem__(self, (dealer, player)):
        return dict.__getitem__(self, (dealer, player))

    def __setitem__(self, (dealer, player), value):
        dict.__setitem__(self, (dealer, player), value)


# An acton value function is just a map from state&action -> value
class ActionValue(defaultdict):
    def __getitem__(self, (dealer, player, action)):
        return dict.__getitem__(self, (dealer, player, action))

    def __setitem__(self, (dealer, player, action), value):
        dict.__setitem__(self, (dealer, player, action), value)


