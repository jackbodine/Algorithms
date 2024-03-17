import numpy as np

T = 1000
As: [int] = [0, 1]
K = len(As)


# Learning Rates
def eta_base(_) -> float:
    return np.sqrt(2 * np.log(K) / T)


def eta_reparameterized(_) -> float:
    return np.sqrt(8 * np.log(K) / T)


def eta_anytime(t: int) -> float:
    return np.sqrt(np.log(K) / t)


def eta_anytime_reparameterized(t: int) -> float:
    return 2 * np.sqrt(np.log(K) / t)


# Algorithm
def hedge(_, eta, sequence):
    sequence_unfolded = []
    regret_at_t = [0]
    cumulative_loss = 0
    cumulative_best_action = 0

    L = [[1 for _ in As]]
    p = [[0 for _ in As]]
    for t in range(1, T):
        p.append([0 for _ in As])
        for action in As:  # calculate p_t(a) for every a
            min_double_a = np.min([L[t - 1][a_double] for a_double in As])
            p[t][action] = np.exp(-eta(t) * (L[t - 1][action]) - min_double_a) / sum(
                [np.exp(-eta(t) * (L[t - 1][a]) - min_double_a) for a in As]
            )

        # Choose action A_t from p_t
        # p_t = np.argmax(p[t])
        p_t = np.random.choice(range(len(As)), p=p[t])

        # Observe losses
        X_t = sequence[t - 1]
        sequence_unfolded.append(X_t)

        l_t = [1 for _ in As]
        l_t[X_t] = 0
        cumulative_loss += l_t[p_t]
        cumulative_best_action += l_t[0]

        next_regret = (cumulative_loss / t) - (sequence_unfolded.count(1) / t)
        regret_at_t.append(cumulative_loss - cumulative_best_action)

        # Update L_t
        L.append([0 for _ in As])
        for a in As:
            L[t][a] = L[t - 1][a] + l_t[a]

    return regret_at_t
