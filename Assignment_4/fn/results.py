from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass(frozen=True)
class Results:
    results: np.ndarray
    num_d_zero: int
    total_mean: float
    ci_total_mean: float
    graph_average: List[float]
    ci_graph: List[float]
    reached_layer_one: np.ndarray
