import numpy as np

p1 = np.genfromtxt('data_policy1.csv', delimiter=',')
p2 = np.genfromtxt('data_policy2.csv', delimiter=',')

time = 25000
gamma = 0.95
states = range(0,5)
def MB_PE(data):
    # print("Running MB_PE...")

    alpha = 1/5

    P_hat = np.zeros((5,5))
    bigN = np.zeros((5,5))
    smallN = np.zeros(5)

    ## Calc P_hat

    for line in data:
        bigN[int(line[0])][int(line[3])] += 1

    for s in states:
        for s_prime in states:
            smallN[s] += bigN[s][s_prime]

    for s in states:
        for s_prime in states:
            P_hat[s][s_prime] = (bigN[s][s_prime] + alpha) / (smallN[s] + alpha * 5)

    r_hat = np.zeros(5)
    ## Calc r_hat
    for s in states:
        reward_sum = sum([line[2] for line in data if int(line[0]) == s])
        r_hat[s] = (alpha + reward_sum) / (alpha + smallN[s])

    # print("P_hat ", P_hat)
    # print("r_hat ", r_hat)

    ## Calc V_hat
    V_hat = np.linalg.inv(np.identity(5) - gamma * P_hat) @ r_hat

    return V_hat
