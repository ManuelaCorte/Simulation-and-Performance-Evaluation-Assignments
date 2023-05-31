from math import ceil
import re
from typing import List
import numpy as np
import scipy.stats as stats
from collections import Counter
import statsmodels.stats.proportion as st

def compute_ci(data, level) -> float:
    std = np.std(data)
    eta = stats.norm.ppf(0.5 + level / 2)
    return eta * std / np.sqrt(len(data))

# We have to take into consideration the fact that the success probability can be quite low or even zero
# so we use the confidence interval provided by scipy which uses Clopper-Pearson method instead of using the normal approximation
def compute_binomial_ci(data, level) -> float:
    n = data.size
    z = n - np.count_nonzero(data)  
    # ci_st = st.proportion_confint(z, n, alpha=1-level, method='beta')
    res = stats.binomtest(z, n, z/n)
    ci = res.proportion_ci(level, method='exact')
    return (ci.high - ci.low)/2

# Each of the samples is a multinomial distribution in 0,1,...,nodes_in_layer
# Since the procedures to compute the confidence interval for the multinomial distribution are quite complex we use bootstrapèing instead
# We could use the normal approximation but it is not very accurate with very high or very low success probability
def compute_multinomial_ci(data, level) -> float:
    # matrix of shape (runs, nodes_in layer)
    reached_nodes_prob = np.sum(data, axis=1) / data.shape[1]
    r0 = 25
    R = ceil((2*r0)/(1-level)) - 1
    means = []
    for r in range(R):
        sample = np.random.choice(reached_nodes_prob, size=reached_nodes_prob.size, replace=True)
        means.append(np.mean(sample))
    means = sorted(means)
    return (means[974] - means[24]) / 2
    # n = data.size
    # z = np.count_nonzero(data)
    # res = stats.binomtest(z, n, z/n)
    # ci = res.proportion_ci(level)
    # return (ci.high - ci.low)/2
    
