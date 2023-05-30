from typing import List
import numpy as np
from scipy import stats

def compute_ci(data, level) -> float:
    std = np.std(data)
    eta = stats.norm.ppf(0.5 + level / 2)
    return eta * std / np.sqrt(len(data))

# We have to take into consideration the fact that the success probability can be quite low or even zero
def compute_multinomial_ci(data, level) -> float:
    # 1 - p probability message doesn't arrive to D
    n = data.size
    z = n - np.count_nonzero(data)  
    res = stats.binomtest(z, n, z/n)
    ci = res.proportion_ci(level)
    return (ci.high - ci.low)/2


def compute_graph_ci(data, level) -> float:
    # foreach layer of the multihop network we find the probability that a message doesn't arrive to D
    eta = stats.norm.ppf(0.5 + level / 2)
    n = data.size
    z = n - np.count_nonzero(data)
    res = stats.binomtest(z, n, z/n)
    ci = res.proportion_ci(level)
    return (ci.high - ci.low)/2
