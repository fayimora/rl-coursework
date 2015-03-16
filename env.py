from random import randint


def draw_black():
    return randint(1, 10)


def draw_red():
    return -randint(1, 10)


def draw_card():
    """black is drwan with probability 2/3"""
    probability = random.random()
    if probability <= float(2) / 3:
        return draw_black()
    else:
        return draw_red()


def is_burst(score):
    return score > 21 or score < 1

