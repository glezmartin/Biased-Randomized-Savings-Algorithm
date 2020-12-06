import numpy as np


def get_random_triangular_position(n):
    position = 0
    while position < 0.5:
        position = (n+1) * (1 - np.sqrt(np.random.random()))
    return int(np.round(position)) - 1


def get_random_geometric_position(n, beta):
    position = 0
    while position < 0.5:
        position = np.log(np.random.random()) / np.log(1 - beta)
        position = position % (n + 1)
    return int(np.round(position)) - 1
