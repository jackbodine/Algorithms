import numpy as np

K = 16


class UCB1:
    def __init__(self, K):
        self.K = K
        self.times_played = [0 for _ in range(K)]
        self.arm_totals = [0 for _ in range(K)]
        self.times_played_log = [0 for _ in range(K)]
        self.arm_totals_log = [0 for _ in range(K)]

        self.incurred_reward = 0
        self.current_regret = 0

    def step(self, t, Alog, reward):

        # Find A_t
        if t < self.K:  # Exploration Phase
            At = t
        else:  # Exploitation Phase
            # Find best A_t to play
            known_empirical_means = [
                self.arm_totals[a] / self.times_played[a] for a in range(self.K)
            ]
            values = [
                known_empirical_means[a]
                + self.K * np.sqrt(np.log(t) / self.times_played[a])
                for a in range(self.K)
            ]
            At = np.argmax(values)

        # Play At
        self.times_played[At] += 1
        self.times_played_log[Alog] += 1

        self.arm_totals_log[Alog] += reward * self.K
        self.arm_totals[At] += reward * self.K

        if At == Alog:
            self.incurred_reward += reward * self.K

        self.current_regret = max(self.arm_totals_log) - self.incurred_reward
