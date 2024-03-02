import numpy as np


class DummyEnv:
    def __init__(self):
        self.nS = 2  # number of states
        self.nA = 2  # number of actions
        self.R = np.array([[0, 1], [1, 0]])  # reward matrix
        self.P = np.array(
            [[[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5]]]
        )  # transition probabilities matrix
