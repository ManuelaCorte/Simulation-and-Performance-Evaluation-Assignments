import numpy as np
import matplotlib.pyplot as plt
from fn.multiple_sim import multiple_sim
from fn.get_data_from_csv import get_data_from_csv

gen = np.random.default_rng(seed=41)

p_axis, d_zero_msg_2_expected_axis, d_zero_msg_5_expected_axis = get_data_from_csv()

runs = 10000
n_steps = 10

d_zero_msg_2_sim_axis = []
d_zero_msg_5_sim_axis = []

r = 2
N = 2
for index, p in enumerate(p_axis):
  runs_when_d_is_zero = multiple_sim(gen, r, N, p, runs)
  runs_when_d_is_zero_perc = runs_when_d_is_zero / runs
  print(f"p error = {p:.3f}, p no msg arrived expect = {d_zero_msg_2_expected_axis[index]:.3f}, sim = {runs_when_d_is_zero_perc:.3f}")
  d_zero_msg_2_sim_axis.append(runs_when_d_is_zero_perc)

r = 5
N = 5
for index, p in enumerate(p_axis):
  runs_when_d_is_zero = multiple_sim(gen, r, N, p, runs)
  runs_when_d_is_zero_perc = runs_when_d_is_zero / runs
  print(f"p error = {p:.3f}, p no msg arrived expect = {d_zero_msg_5_expected_axis[index]:.3f}, sim = {runs_when_d_is_zero_perc:.3f}")
  d_zero_msg_5_sim_axis.append(runs_when_d_is_zero_perc)

plt.figure()
plt.plot(p_axis, d_zero_msg_2_sim_axis)
plt.plot(p_axis, d_zero_msg_2_expected_axis)
plt.figure()
plt.plot(p_axis, d_zero_msg_5_sim_axis)
plt.plot(p_axis, d_zero_msg_5_expected_axis)
plt.show()