from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass(frozen=True)
class Results:
    results: np.ndarray  # wheter or not the message reached the node for each run
    num_d_zero: int  # number of runs where the message reached the last row
    total_mean: float  # percentage of runs where the message reached the last row
    ci_total_mean: float
    graph_average: List[float]  # average number of nodes reached for each layer
    ci_graph: List[float]
    reached_layer_one: np.ndarray  # number of nodes reache in layer 1 for each run (used for post stratification)
