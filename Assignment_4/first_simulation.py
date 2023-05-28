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
msg_2_graph_avgs = []
msg_5_graph_avgs = []
msg_2_graph_cis = []
msg_5_graph_cis = []

r = 2
N = 2
for p in probabilities:
    results_2_sim = multiple_sim(gen, r, N, p, runs)
    d_zero_msg_2_sim_axis.append(results_2_sim.total_mean)
    d_zero_msg_2_sim_ci.append(results_2_sim.ci_total_mean)


r = 5
N = 5
for p in probabilities:
    results_5_sim = multiple_sim(gen, r, N, p, runs)
    d_zero_msg_5_sim_axis.append(results_5_sim.total_mean)
    d_zero_msg_5_sim_ci.append(results_5_sim.ci_total_mean)

f, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.errorbar(
    probabilities,
    d_zero_msg_2_sim_axis,
    yerr=d_zero_msg_2_sim_ci,
    label="r = 2, N = 2",
    linestyle="dotted",
    marker="o",
    markersize=2,
)
ax.errorbar(
    probabilities,
    d_zero_msg_5_sim_axis,
    yerr=d_zero_msg_5_sim_ci,
    label="r = 5, N = 5",
    linestyle="dotted",
    marker="o",
    markersize=2,
)
ax.set_title("error rates")
ax.set_xlabel("p")
ax.set_ylabel("p no message arrived to D")
ax.legend()

plt.tight_layout()
plt.show()
