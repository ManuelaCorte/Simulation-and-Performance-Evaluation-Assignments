import numpy as np
import matplotlib.pyplot as plt
from fn.get_data_from_csv import get_data_from_csv
from fn.multiple_sim import multiple_sim

gen = np.random.default_rng(seed=41)
probabilities = np.arange(0, 1.1, 0.1)

p_axis, d_zero_msg_2_expected_axis, d_zero_msg_5_expected_axis = get_data_from_csv()

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
    results_2_sim = multiple_sim(r, N, p, runs, extended=True)
    d_zero_msg_2_sim_axis.append(results_2_sim.total_mean)
    d_zero_msg_2_sim_ci.append(results_2_sim.ci_total_mean)
    msg_2_graph_avgs.append(results_2_sim.graph_average)
    msg_2_graph_cis.append(results_2_sim.ci_graph)


r = 5
N = 5
for p in probabilities:
    results_5_sim = multiple_sim(r, N, p, runs, extended=True)
    d_zero_msg_5_sim_axis.append(results_5_sim.total_mean)
    d_zero_msg_5_sim_ci.append(results_5_sim.ci_total_mean)
    msg_5_graph_avgs.append(results_5_sim.graph_average)
    msg_5_graph_cis.append(results_5_sim.ci_graph)

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
ax.plot(p_axis, d_zero_msg_2_expected_axis, label="r = 2, N = 2 theoretical")
ax.plot(p_axis, d_zero_msg_5_expected_axis, label="r = 5, N = 5 theoretical")
ax.set_title("error rates")
ax.set_xlabel("p")
ax.set_ylabel("p no message arrived to D")
ax.legend()

f, ax = plt.subplots(1, 1, figsize=(20, 25))
for index, p in enumerate(probabilities):
    ax.errorbar(
        np.arange(1, 3),
        msg_2_graph_avgs[index],
        yerr=msg_2_graph_cis[index],
        label=f"p: {p:.2f}",
        linestyle="dotted",
        marker="o",
        markersize=2,
    )
ax.set_title(f"average reached nodes per layer r = 2, N = 2")
ax.set_xlabel("r")
ax.set_ylabel("avg # nodes")
ax.set_xticks(np.arange(1, 3))

ax.legend()

f, ax = plt.subplots(1, 1)
for index, p in enumerate(probabilities):
    ax.errorbar(
        np.arange(1, 6),
        msg_5_graph_avgs[index],
        yerr=msg_5_graph_cis[index],
        label=f"p: {p:.2f}",
        linestyle="dotted",
        marker="o",
        markersize=2,
    )
ax.set_title(f"average reached nodes per layer r = 5, N = 5")
ax.set_xlabel("r")
ax.set_ylabel("avg # nodes")
ax.set_xticks(np.arange(1, 6))
ax.legend()

plt.show()
