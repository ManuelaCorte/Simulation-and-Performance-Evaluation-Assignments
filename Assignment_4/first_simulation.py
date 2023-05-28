from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt
from fn.multiple_sim import multiple_sim

gen = np.random.default_rng(seed=41)
probabilities = np.arange(0.0, 1.0, 0.05)

runs = 1000

d_zero_msg_2_sim_axis = []
d_zero_msg_2_sim_ci = []
d_zero_msg_5_sim_axis = []
d_zero_msg_5_sim_ci = []

r = 2
N = 2
for p in probabilities:
    runs_when_d_is_zero, mean, ci = multiple_sim(gen, r, N, p, runs)
    d_zero_msg_2_sim_axis.append(mean)
    d_zero_msg_2_sim_ci.append(ci)

r = 5
N = 5
for p in probabilities:
    runs_when_d_is_zero, mean, ci = multiple_sim(gen, r, N, p, runs)
    d_zero_msg_5_sim_axis.append(mean)
    d_zero_msg_5_sim_ci.append(ci)

f, ax = plt.subplots(1, 1, figsize=(10,10))
ax.errorbar(probabilities, d_zero_msg_2_sim_axis, yerr=d_zero_msg_2_sim_ci, label='r = 2, N = 2', linestyle='dotted', marker='o', markersize=2)
ax.errorbar(probabilities, d_zero_msg_5_sim_axis, yerr=d_zero_msg_5_sim_ci, label='r = 5, N = 5', linestyle='dotted', marker='o', markersize=2)
ax.set_title('error rates')
ax.set_xlabel('p')
ax.set_ylabel('p no message arrived to D')
ax.legend()

plt.tight_layout()
plt.show()