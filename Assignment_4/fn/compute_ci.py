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
    res = stats.binomtest(z, n, z / n)
    ci = res.proportion_ci(level, method="exact")
    return (ci.high - ci.low) / 2


# Each of the samples is a multinomial distribution in 0,1,...,nodes_in_layer
# Since the procedures to compute the confidence interval for the multinomial distribution are quite complex we use bootstrapèing instead
# We could use the normal approximation but it is not very accurate with very high or very low success probability
def compute_multinomial_ci_boostrap(data, level) -> float:
    # matrix of shape (runs, nodes_in layer)
    reached_nodes_prob = np.sum(data, axis=1) / data.shape[1]
    r0 = 25
    R = ceil((2 * r0) / (1 - level)) - 1
    means = []
    for r in range(R):
        sample = np.random.choice(
            reached_nodes_prob, size=reached_nodes_prob.size, replace=True
        )
        means.append(np.mean(sample))
    means = sorted(means)
    return (means[974] - means[24]) / 2


# Multinomial confidence interval computed as a binomial (probably wrong)
def compute_multinomial_ci(data, level) -> float:
    n = data.size
    z = np.count_nonzero(data)
    res = stats.binomtest(z, n, z / n)
    ci = res.proportion_ci(level)
    return (ci.high - ci.low) / 2


# https://en.wikipedia.org/wiki/Stratified_sampling
# We use the number of nodes reached in layer one as the stratification variable
# We know the theoretical distribution of this value as each link is a bernoulli distribution of parameter 1-p
# So overall the number of nodes reached in layer one is a binomial distribution of parameters N and 1-p
# Since we can't use the provivded confidence interval for the binomial that adjusts for the fact that the number of successes can the very low 
# we use the rule of three method to compute the confidence interval
def compute_ci_stratification(data, level, n_th, n) -> float:
    n_stratus = len(data)
    n_sim = [len(data[i]) for i in range(n_stratus)]
    # print(f'n_sim: {n_sim} n_th: {n_th} n: {n} n_stratus: {n_stratus}')
    stratum_var = [np.var(data[i]) for i in range(n_stratus)]
    var = np.sum(
        (n_th[i] / n) ** 2 * (stratum_var[i] / n_sim[i]) for i in range(n_stratus)
    )
    if var == 0:
        return 3/np.sum(n_sim)
    eta = stats.norm.ppf(1 - (1 - level) / 2)
    return eta * np.sqrt(var / n_stratus)
