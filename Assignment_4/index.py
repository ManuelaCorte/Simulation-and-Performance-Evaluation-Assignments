import numpy as np
import matplotlib.pyplot as plt
from fn.multiple_sim import multiple_sim
from fn.get_data_from_csv import get_data_from_csv

gen = np.random.default_rng(seed=41)
r = 5
N = 5

p_axis, d_zero_2_axis, d_zero_5_axis = get_data_from_csv()

runs = 10000
n_steps = 10

y = []

for index, p in enumerate(p_axis):
  runs_when_d_is_zero = multiple_sim(gen, r, N, p, runs)
  runs_when_d_is_zero_perc = runs_when_d_is_zero / runs
  print(f"p error = {p:.3f}, p no msg arrived expect = {d_zero_5_axis[index]:.3f}, sim = {runs_when_d_is_zero_perc:.3f}")
  y.append(runs_when_d_is_zero_perc)

plt.plot(p_axis, y)
plt.plot(p_axis, d_zero_5_axis)
plt.show()