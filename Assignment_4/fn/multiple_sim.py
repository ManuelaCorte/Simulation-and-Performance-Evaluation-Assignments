from fn.sim import sim

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