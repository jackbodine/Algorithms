import numpy as np


def follow_the_leader(seq):
    # Two actions: 0 and 1. Always taking 0 is optimal

    arm_totals = [0, 0]
    FTL_choices = []

    FTL_loss_cumulative = 0
    cumulative_best_action = 0

    regret_at_t = [0]

    for t in range(1, len(seq)):
        FTL_choices.append(np.argmax(arm_totals))

        if FTL_choices[-1] != seq[t - 1]:
            FTL_loss_cumulative += 1

        if 0 != seq[t - 1]:
            cumulative_best_action += 1

        regret_at_t.append(FTL_loss_cumulative - cumulative_best_action)

        arm_totals[seq[t - 1]] += 1

    return regret_at_t
