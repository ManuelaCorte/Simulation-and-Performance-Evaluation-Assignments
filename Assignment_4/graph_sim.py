import numpy as np
gen = np.random.default_rng(seed=41)

logging = True

r = 5
N = 5
p = 0.5

def count_positive_elem(arr, dim):
  count = 0
  for i in range(dim):
    if arr[i] < 1: continue
    count += 1
  return count

# expected
expected_nodes_with_msg_per_row = [(1-p) * N]
for i in range(r):
  expected_nodes_with_msg_per_row.append((1 - (p ** expected_nodes_with_msg_per_row[i])) * N)
expected_msg_arrived_to_d = (1-p) * expected_nodes_with_msg_per_row[r-1]

def sim(r, N, p, logging = False, expected_nodes_with_msg_per_row = 0.0, expected_msg_arrived_to_d = 0.0):
  # n messages each node received
  graph_msgs = np.zeros((r, N))

  if logging:
    print('init')
    print(graph_msgs)
    input()

  # launch from S
  for j in range(N):
    if gen.uniform() < p: 
      if logging: print(f"message passing from S to {0},{j} failed")
      continue
    graph_msgs[0][j] += 1

  if logging:
    print('from S')
    new_nodes_with_msg = count_positive_elem(graph_msgs[0], N)
    print(f"nodes with msg at row {0} expected {expected_nodes_with_msg_per_row[0]:.2f}, found {new_nodes_with_msg}")
    print(graph_msgs)
    input()

  # launch to next row
  for i in range(r-1):
    for j in range(N):
      if graph_msgs[i][j] < 1: continue
      # pass the message to each node in the next row
      for h in range(N):
        if gen.uniform() < p: 
          if logging: print(f"message passing from {i},{j} to {i+1},{h} failed")
          continue
        graph_msgs[i+1][h] += 1
    
    if logging:
      old_nodes_with_msg = count_positive_elem(graph_msgs[i], N)
      new_nodes_with_msg = count_positive_elem(graph_msgs[i+1], N)
      new_nodes_with_msg_expected_now = (1 - (p ** old_nodes_with_msg)) * N
      print(f"nodes with msg at row {i} expected {expected_nodes_with_msg_per_row[i]:.2f}, expected now {new_nodes_with_msg_expected_now:.2f}, found {new_nodes_with_msg}")

      print(f'row {i} passed to row {i+1}')
      print(graph_msgs)
      input()

  # launch to D
  d_msgs = 0
  for j in range(N):
    if graph_msgs[r-1][j] < 1: continue
    if gen.uniform() < p: 
      if logging: print(f"message passing from {r-1},{j} to D failed")
      continue
    d_msgs += 1

  if logging:
    print('final')
    print(graph_msgs)
    input()
    print(f"expected messages arrived to D {expected_msg_arrived_to_d:.2f}, found {d_msgs}")
  return d_msgs

runs = 100000
sum = 0
runs_when_d_is_zero = 0
for _x in range(runs):
  new_sim = sim(r, N, p)
  sum += new_sim
  if new_sim < 1: runs_when_d_is_zero += 1

mean = sum / runs
print(f"msgs arrived to D: theoretical {expected_msg_arrived_to_d:.2f}, simulated mean {mean:.2f}")
runs_when_d_is_zero_perc = runs_when_d_is_zero/runs*100
print(f"number of runs where d is zero is {runs_when_d_is_zero} ({runs_when_d_is_zero_perc:.2f}%)")