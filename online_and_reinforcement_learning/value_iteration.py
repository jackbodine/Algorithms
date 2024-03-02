import numpy as np


def value_iteration(env, gamma=0.90, epsilon=(10 ** -6)):
    """
    Value Iteration is a reinforcement learning algorithm used in Markov Decision Processes to find the optimal policy
    by iteratively updating the values of all states towards the maximum expected return. It employs the Bellman
    Equation to calculate the best possible value of each state, considering all possible actions,
    the subsequent states, and the immediate plus discounted future rewards. This process repeats until the
    value function changes minimally between iterations, indicating convergence to an optimal solution.

    :param env: a markov decision process representing the environment.
    :param gamma: discount factor
    :param epsilon: threshold for convergence
    :return: an optimal policy for the environment
    """

    n = 0
    V0 = [0 for _ in range(env.nS)]
    V1 = [np.max(rMax, axis=0) / (1 - gamma) for rMax in env.R]

    Vs = [V0, V1]
    bound = (epsilon * (1 - gamma)) / (2 * gamma)
    while np.linalg.norm(np.subtract(Vs[n + 1], Vs[n]), ord=np.inf) >= bound:

        newV = [0 for _ in range(env.nS)]
        for s in range(env.nS):
            actions = []
            for a in range(env.nA):
                actions.append(
                    env.R[s, a]
                    + (gamma * sum([u * p for (u, p) in zip(Vs[n], env.P[s, a])]))
                )
            newV[s] = max(actions)

        Vs.append(newV)
        n += 1

    result = np.zeros(env.nS)
    for s in range(env.nS):
        actions = []
        for a in range(env.nA):
            actions.append(
                env.R[s, a]
                + (gamma * sum([u * p for (u, p) in zip(Vs[n], env.P[s, a])]))
            )
        result[s] = actions.index(max(actions))

    return result
