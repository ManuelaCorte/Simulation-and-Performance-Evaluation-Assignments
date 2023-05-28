from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Results:
    num_d_zero: int
    total_mean: float
    ci_total_mean: float
    graph_average: List[float]
    ci_graph: List[float]
