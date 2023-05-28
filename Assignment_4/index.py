import numpy as np
import matplotlib.pyplot as plt
from fn.multiple_sim import multiple_sim
from fn.get_data_from_csv import get_data_from_csv

gen = np.random.default_rng(seed=41)

p_axis, d_zero_msg_2_expected_axis, d_zero_msg_5_expected_axis = get_data_from_csv()

runs = 1000

d_zero_msg_2_sim_axis = []
d_zero_msg_5_sim_axis = []

r = 2
N = 2
for index, p in enumerate(p_axis):
    runs_when_d_is_zero, mean, ci = multiple_sim(gen, r, N, p, runs)
    print(
        f"p error = {p:.3f}, p no msg arrived expect = {d_zero_msg_2_expected_axis[index]:.3f}, sim = {mean:.3f} +- {ci:.3f}"
    )
    d_zero_msg_2_sim_axis.append(mean)

r = 5
N = 5
for index, p in enumerate(p_axis):
    runs_when_d_is_zero, mean, ci = multiple_sim(gen, r, N, p, runs)
    print(
        f"p error = {p:.3f}, p no msg arrived expect = {d_zero_msg_5_expected_axis[index]:.3f}, sim = {mean:.3f} +- {ci:.3f}"
    )
    d_zero_msg_5_sim_axis.append(mean)


f, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.plot(p_axis, d_zero_msg_2_sim_axis, label="simulated value")
ax.plot(p_axis, d_zero_msg_2_expected_axis, label="theoretical value")
ax.set_title("error rates, r = 2, N = 2")
ax.set_xlabel("p")
ax.set_ylabel("p no message arrived to D")
ax.legend()

f, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.plot(p_axis, d_zero_msg_5_sim_axis, label="simulated value")
ax.plot(p_axis, d_zero_msg_5_expected_axis, label="theoretical value")
ax.set_title("error rates, r = 5, N = 5")
ax.set_xlabel("p")
ax.set_ylabel("p no message arrived to D")
ax.legend()

plt.show()
