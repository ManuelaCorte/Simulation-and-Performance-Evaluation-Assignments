from numpy import dtype
from fn.compute_ci import compute_multinomial_ci, compute_graph_ci
from fn.results import Results
from fn.sim import sim
import numpy as np


def multiple_sim(gen, r, N, p, runs, logging=False):
    # expected
    expected_nodes_with_msg_per_row = [(1 - p) * N]
    for i in range(r):
        expected_nodes_with_msg_per_row.append(
            (1 - (p ** expected_nodes_with_msg_per_row[i])) * N
        )
    expected_msg_arrived_to_d = (1 - p) * expected_nodes_with_msg_per_row[r - 1]

    sum = 0
    results = []
    graphs = np.zeros(shape=(runs, r, N))
    runs_when_d_is_zero = 0

    for i in range(runs):
        new_sim, msg_graph = sim(gen, r, N, p)
        msg_graph = np.ma.make_mask(msg_graph, copy=True).astype(dtype=np.float16)
        graphs[i] = msg_graph
        sum += new_sim
        if new_sim < 1:
            runs_when_d_is_zero += 1
        results.append(new_sim)

    runs_when_d_is_zero_perc = runs_when_d_is_zero / runs
    ci = compute_multinomial_ci(results, 0.95)

    graph_average = np.mean(graphs, axis=0)
    ci_graph = [compute_graph_ci(graphs[:, i, :], 0.95) for i in range(N)]

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
