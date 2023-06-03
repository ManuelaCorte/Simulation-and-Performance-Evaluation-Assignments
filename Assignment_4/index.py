import numpy as np
import matplotlib.pyplot as plt
from fn.multiple_sim import multiple_sim
from fn.get_data_from_csv import get_data_from_csv

p_axis, d_zero_msg_2_expected_axis, d_zero_msg_5_expected_axis = get_data_from_csv()

runs = 1000

d_zero_msg_2_sim_axis = []
d_zero_msg_5_sim_axis = []
msg_2_sim_ci = []
msg_5_sim_ci = []
results_2_sim = {}
results_5_sim = {}

r = 2
N = 2
for index, p in enumerate(p_axis):
    results_2_sim = multiple_sim(r, N, p, runs)
    print(
        f"p error = {p:.3f}, p no msg arrived expect = {d_zero_msg_2_expected_axis[index]:.3f}, sim = {results_2_sim.total_mean:.3f} +- {results_2_sim.ci_total_mean:.3f}"
    )
    d_zero_msg_2_sim_axis.append(results_2_sim.total_mean)
    msg_2_sim_ci.append(results_2_sim.ci_total_mean)

r = 5
N = 5
for index, p in enumerate(p_axis):
    results_5_sim = multiple_sim(r, N, p, runs)
    print(
        f"p error = {p:.3f}, p no msg arrived expect = {d_zero_msg_5_expected_axis[index]:.3f}, sim = {results_5_sim.total_mean:.3f} +- {results_5_sim.ci_total_mean:.3f}"
    )
    d_zero_msg_5_sim_axis.append(results_5_sim.total_mean)
    msg_5_sim_ci.append(results_5_sim.ci_total_mean)


f, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.errorbar(
    p_axis,
    d_zero_msg_2_sim_axis,
    yerr=msg_2_sim_ci,
    linestyle="dotted",
    marker="o",
    markersize=2,
    label="simulation r=2 N=2",
)
ax.plot(p_axis, d_zero_msg_2_expected_axis, label="theoretical r=2 N=2")
ax.errorbar(
    p_axis,
    d_zero_msg_5_sim_axis,
    yerr=msg_5_sim_ci,
    linestyle="dotted",
    marker="o",
    markersize=2,
    label="simulation r=5 N=5",
)
ax.plot(p_axis, d_zero_msg_5_expected_axis, label="theoretical r=5 N=5")
ax.set_title("error rates")
ax.set_xlabel("p")
ax.set_ylabel("p no message arrived to D")
ax.legend()

plt.show()
