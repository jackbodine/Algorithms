import matplotlib.pyplot as plt
import numpy
import numpy as np

p1 = np.genfromtxt('data_policy1.csv', delimiter=',')
p2 = np.genfromtxt('data_policy2.csv', delimiter=',')

time = 25000
gamma = 0.95
states = range(0, 5)


def a(t, _):
    return 10 / ((t ** (2 / 3)) + 1)


def b(t, sumForS):
    return 10 / (sumForS ** (7 / 9) + 1)


def TD(data, func):
    # print("Running TD...")
    # print(max(data[2]))
    V = numpy.zeros((1, 5))
    occuranceSums = numpy.zeros(5)

    for t, line in enumerate(data):
        Vplus1 = numpy.zeros(5)
        # print(line[0])
        occuranceSums[int(line[0])] += 1

        for s in states:
            if line[0] == s:
                Vplus1[s] = V[t][s] + (
                        func(t + 1, occuranceSums[s]) * (line[2] + (gamma * V[t][int(line[3])]) - V[t][s]))
            else:
                Vplus1[s] = V[t][s]

        V = numpy.vstack([V, Vplus1])
    return V[-1]
