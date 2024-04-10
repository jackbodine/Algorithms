import numpy as np

K = 16


def learning_rate(t):
    return np.sqrt(np.log(K) / (K * K * t))


class EXP3:
    def __init__(self, K):
        self.K = K
        self.L_tilda = [[0 for _ in range(K)]]
        self.t = 0
        self.alg_loss_total = 0
        self.opt_loss_total = [0 for _ in range(K)]
        self.regret = 0

    def step(self, logged_choice, reward):
        self.t += 1
        lr = learning_rate(self.t, self.K)

        # Calc Distribution
        min_double_a = np.min(
            [self.L_tilda[-1][a_double] for a_double in range(self.K)]
        )
        denominator = np.sum(
            [np.exp(-lr * (self.L_tilda[-1][a] - min_double_a)) for a in range(self.K)]
        )
        p_not_logging = [
            np.exp(-lr * (self.L_tilda[-1][a] - min_double_a)) / denominator
            for a in range(self.K)
        ]

        A_t = np.random.choice(range(self.K), p=p_not_logging)
        l = (1 - reward) * self.K

        loss_tilda = [0 for _ in range(self.K)]
        loss_tilda[A_t] = (l) * (logged_choice == A_t) / p_not_logging[A_t]

        self.L_tilda.append(
            [self.L_tilda[-1][a] + loss_tilda[a] for a in range(self.K)]
        )

        # Regret Calculations
        self.alg_loss_total += l * (logged_choice == A_t)
        self.opt_loss_total[logged_choice] += l
        self.regret = self.alg_loss_total - min(self.opt_loss_total)
