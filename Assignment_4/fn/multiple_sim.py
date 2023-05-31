from numpy import dtype
from fn.compute_ci import compute_multinomial_ci, compute_binomial_ci
from fn.results import Results
from fn.sim import sim
import numpy as np


def multiple_sim(r, N, p, runs, logging=False, extended=False):
    # expected
    seeds = np.random.default_rng(seed=42) 
    seed = int(seeds.uniform(0, 1000000))
    gen = np.random.default_rng(seed=seed)
    expected_nodes_with_msg_per_row = [(1 - p) * N]
    for i in range(r):
        expected_nodes_with_msg_per_row.append(
            (1 - (p ** expected_nodes_with_msg_per_row[i])) * N
        )
    expected_msg_arrived_to_d = (1 - p) * expected_nodes_with_msg_per_row[r - 1]

    sum = 0
    results = np.zeros(shape=(runs, 1))
    graphs = np.zeros(shape=(runs, r, N))
    runs_when_d_is_zero = 0
    
    for i in range(runs):
        new_sim, msg_graph = sim(gen, r, N, p)
        if extended:
            msg_graph = np.ma.make_mask(msg_graph, copy=True).astype(dtype=np.float16)
            graphs[i] = msg_graph
        sum += new_sim
        if new_sim < 1:
            runs_when_d_is_zero += 1
        results[i] = new_sim

    runs_when_d_is_zero_perc = runs_when_d_is_zero / runs
    ci = compute_binomial_ci(results, 0.95)

    if extended:
        graph_average = [np.sum(graphs[:, i, :]) / runs for i in range(r)]
        ci_graph = [compute_multinomial_ci(graphs[:, i, :], 0.95) for i in range(r)]
    else:
        graph_average = []
        ci_graph = []
    if logging:
        mean = sum / runs
        print(
            f"msgs arrived to D: theoretical {expected_msg_arrived_to_d:.2f}, simulated mean {mean:.2f}"
        )
        print(
            f"number of runs where d is zero is {runs_when_d_is_zero} ({runs_when_d_is_zero_perc:.2f}%)"
        )

    res = Results(
        runs_when_d_is_zero, runs_when_d_is_zero_perc, ci, graph_average, ci_graph
    )
    return res
