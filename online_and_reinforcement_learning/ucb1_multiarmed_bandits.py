import numpy as np
import math
import matplotlib.pyplot as plt

K = 2
T = 100000

for DELTA in [1 / 4, 1 / 8, 1 / 16]:

    current_rewards = [0 for _ in range(K)]

    def genRewards():
        global current_rewards

        current_rewards[0] = np.random.binomial(
            size=1, n=1, p=0.5 + (0.5 * DELTA)
        )  # gen a*
        current_rewards[1] = np.random.binomial(
            size=1, n=1, p=0.5 - (0.5 * DELTA)
        )  # gen a

    ### BEGIN UCB ###
    regret = []
    opt_regret = []
    for run in range(20):

        regret.append([])
        opt_regret.append([])

        times_played = [0 for _ in range(K)]
        arm_totals = [0 for _ in range(K)]
        delta_values = []

        opt_times_played = [0 for _ in range(K)]
        opt_arm_totals = [0 for _ in range(K)]
        opt_delta_values = []

        for t in range(T):
            genRewards()
            At = -1
            opt_At = -1

            if t < K:  # Exploration Phase
                At = t
                opt_At = t
            else:  # Exploitation Phase
                # Find best A_t to play
                max_function_values = [
                    (arm_totals[i] / times_played[i])
                    + (math.sqrt((3 * math.log(t)) / (2 * times_played[i])))
                    for i in range(K)
                ]
                At = max_function_values.index(max(max_function_values))  # arg max
                opt_max_function_values = [
                    (opt_arm_totals[i] / opt_times_played[i])
                    + (math.sqrt((math.log(t)) / (opt_times_played[i])))
                    for i in range(K)
                ]
                opt_At = opt_max_function_values.index(max(opt_max_function_values))

            # Play A_t
            times_played[At] += 1
            arm_totals[At] += current_rewards[At]
            # arm_totals[0] += current_rewards[0]
            # arm_totals[1] += current_rewards[1]

            opt_times_played[opt_At] += 1
            opt_arm_totals[opt_At] += current_rewards[opt_At]

            # Calc Delta
            delta_values.append(
                max(
                    (arm_totals[0] / times_played[0]),
                    arm_totals[1] / max(times_played[1], 1),
                )
                - (arm_totals[At] / times_played[At])
            )
            opt_delta_values.append(
                max(
                    (opt_arm_totals[0] / opt_times_played[0]),
                    opt_arm_totals[1] / max(opt_times_played[1], 1),
                )
                - (opt_arm_totals[opt_At] / opt_times_played[opt_At])
            )

            if t == 0:
                regret[run].append(delta_values[At])
                opt_regret[run].append(opt_delta_values[opt_At])
            else:
                regret[run].append(regret[run][t - 1] + delta_values[At])
                opt_regret[run].append(
                    opt_regret[run][t - 1] + opt_delta_values[opt_At]
                )

        # print(arm_totals)
        # print(times_played)
        # print(opt_times_played)
        # print(delta_values)
        # print(reward_history)

    ### Plot Regret
    avg_regrets = np.mean(np.array(regret), axis=0)
    deviation = np.std(np.array(regret), axis=0)
    opt_avg_regrets = np.mean(np.array(opt_regret), axis=0)
    opt_deviation = np.std(np.array(opt_regret), axis=0)
    plt.plot(avg_regrets, label="UCB1", color="blue")
    plt.plot(
        avg_regrets + deviation,
        label="UCB1 Standard Deviation",
        color="blue",
        linestyle="dashed",
    )
    plt.plot(opt_avg_regrets, label="UCB1 Optimized", color="orange")
    plt.plot(
        opt_avg_regrets + opt_deviation,
        label="UCB1 Optimized Standard Deviation",
        color="orange",
        linestyle="dashed",
    )

    # Different type of bounds.
    # plt.fill_between(range(T), avg_regrets + deviation, avg_regrets, alpha=.5, linewidth=0)
    # plt.fill_between(range(T), opt_avg_regrets + opt_deviation, opt_avg_regrets, alpha=.5, linewidth=0)
    plt.title(f"Average Regret for UCB1 over 20 Runs, Delta = {DELTA}")
    plt.ylabel("Average Regret")
    plt.xlabel("Rounds Played")
    plt.legend(loc="upper left")
    plt.show()

print("DONE")
