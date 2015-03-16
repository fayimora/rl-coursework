from collections import defaultdict

HIT, STICK = 1, 0

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

    # converts an action value function to a value function by
    # simply creating a new value function and adding either the value
    # of hitting ir sticking, deending on which is better
    def to_value_function(self):
        value_function = Value(float)
        keys = self.keys()

        for key in keys:
            dealer, player, action = key[0], key[1], key[2]
            hit_value = self.get((dealer, player, HIT))
            stick_value = self.get((dealer, player, STICK))

            if hit_value > stick_value:
                value_function[(dealer, player)] = hit_value
            else:
                value_function[(dealer, player)] = stick_value

        return value_function


