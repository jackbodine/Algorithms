import numpy as np

T = 1000
K = 10


def eta_anytime(t: int) -> float:
    return np.sqrt(np.log(K) / (t * K))


def EXP3(_, eta, sequence):
    regret_at_t = [0]
    cumulative_loss = 0
    cumulative_best_action = 0

    L = [[1 for _ in range(K)]]
    p = [[0 for _ in range(K)]]
    for t in range(1, T):
        p.append([0 for _ in range(K)])
        for action in range(K):  # calculate p_t(a) for every a
            min_double_a = np.min([L[t - 1][a_double] for a_double in range(K)])
            p[t][action] = np.exp(-eta(t) * (L[t - 1][action]) - min_double_a) / sum(
                [np.exp(-eta(t) * (L[t - 1][a]) - min_double_a) for a in range(K)]
            )

        # Choose action A_t from p_t
        p_t = np.random.choice(range(K), p=p[t])

        # Observe losses
        winning_bandit = sequence[t - 1]

        l_tA_t = 0 if winning_bandit == p_t else 1
        cumulative_loss += l_tA_t
        cumulative_best_action += 0 if winning_bandit == 0 else 1

        regret_at_t.append(cumulative_loss - cumulative_best_action)

        # Update L_t
        L.append([0 for _ in range(K)])
        for a in range(K):
            L[t][a] = L[t - 1][a] + ((l_tA_t if a == p_t else 0) / p[t][a])

    return regret_at_t
