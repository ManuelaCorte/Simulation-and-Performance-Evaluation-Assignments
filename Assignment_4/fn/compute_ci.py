from typing import List
import numpy as np
from scipy import stats


def compute_ci(data, level) -> float:
    std = np.std(data)
    eta = stats.norm.ppf(0.5 + level / 2)
    return eta * std / np.sqrt(len(data))


def compute_multinomial_ci(data, level) -> float:
    # Select elements from array equal to 0
    counts = [x for x in data if x == 0]
    p = len(counts) / len(data)
    se = np.sqrt(p * (1 - p) / len(data))  # standard error
    eta = stats.norm.ppf(0.5 + level / 2)
    return eta * se


def compute_graph_ci(data, level) -> float:
    counts = [type(x) for x in data[:,][0] if x == 0]
    p = len(counts) / len(data[:,])
    se = np.sqrt(p * (1 - p) / len(data[:,]))
    eta = stats.norm.ppf(0.5 + level / 2)
    return eta * se
