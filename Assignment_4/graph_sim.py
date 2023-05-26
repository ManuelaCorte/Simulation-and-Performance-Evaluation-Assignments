import numpy as np
import matplotlib.pyplot as plt
from fn.sim import sim
gen = np.random.default_rng(seed=41)

logging = True

r = 5
N = 5
# p = 0.5
runs = 10000

def multiple_sim(gen, r, N, p, runs, logging=False):
  # expected
  expected_nodes_with_msg_per_row = [(1-p) * N]
  for i in range(r):
    expected_nodes_with_msg_per_row.append((1 - (p ** expected_nodes_with_msg_per_row[i])) * N)
  expected_msg_arrived_to_d = (1-p) * expected_nodes_with_msg_per_row[r-1]

  sum = 0
  runs_when_d_is_zero = 0
  for _x in range(runs):
    new_sim = sim(gen, r, N, p)
    sum += new_sim
    if new_sim < 1: runs_when_d_is_zero += 1

  if logging:
    mean = sum / runs
    print(f"msgs arrived to D: theoretical {expected_msg_arrived_to_d:.2f}, simulated mean {mean:.2f}")
    runs_when_d_is_zero_perc = runs_when_d_is_zero / runs * 100
    print(f"number of runs where d is zero is {runs_when_d_is_zero} ({runs_when_d_is_zero_perc:.2f}%)")
  return runs_when_d_is_zero

n_steps = 50
x = []
y = []
for p_int in range(int(1 * n_steps) + 1):
  p = p_int / n_steps
  runs_when_d_is_zero = multiple_sim(gen, r, N, p, runs)
  runs_when_d_is_zero_perc = runs_when_d_is_zero / runs
  print(f"p error = {p:.3f}, \t p no msg arrived = {runs_when_d_is_zero_perc}")
  x.append(p)
  y.append(runs_when_d_is_zero_perc)
plt.plot(x, y)
plt.show()