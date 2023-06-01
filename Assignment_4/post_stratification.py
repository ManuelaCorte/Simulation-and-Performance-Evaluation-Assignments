# We use the number of nodes reached in layer one as the stratification variable
# We know the theoretical distribution of this value as each link is a bernoulli distribution of parameter 1-p
# So overall the number of nodes reached in layer one is a binomial distribution of parameters N and 1-p

from math import e
import numpy as np
from fn.get_data_from_csv import get_data_from_csv
from fn.multiple_sim import multiple_sim
import scipy.stats as stats
import matplotlib.pyplot as plt

# https://en.wikipedia.org/wiki/Stratified_sampling
def compute_ci(data, level, n_th, n) -> float:
    n_stratus = len(data)
    n_sim = [len(data[i]) for i in range(n_stratus)]
    # print(f'n_sim: {n_sim} n_th: {n_th} n: {n} n_stratus: {n_stratus}')
    stratum_var = [np.var(data[i]) for i in range(n_stratus)]
    var = np.sum((n_th[i]/n)**2 * (stratum_var[i] / n_sim[i]) for i in range(n_stratus))
    # print(f'var: {var}')
    eta = stats.norm.ppf(1-(1-level)/2)
    return eta*np.sqrt(var/n_stratus)

p_axis, d_zero_msg_2_expected_axis, d_zero_msg_5_expected_axis = get_data_from_csv()

runs = 1000
probs = np.arange(0, 1, 0.1)

r = 2
N = 2


est_2 = []
est_2_ci = []
est_2_strat = []
est_2_strat_ci = []

for p in probs:
    stratified_2 = []
    res = multiple_sim(r, N, p, runs, extended=True)

    binom = stats.binom(N, 1-p)
    p_th = binom.pmf(range(N+1))
    n_th = p_th*runs
    # print(f'p_th: {p_th}')

    for i in range(N+1):
        stratified_2.append(res.results[res.reached_layer_one == i])
    
    p_est = [len(stratified_2[i])/runs for i in range(N+1)]
    p_est = np.array(p_est)
    # print(f'p: {p_est}')

    stratified_2_means = [np.mean(stratified_2[i]) for i in range(N+1)]
    est = 1/runs * np.sum([n_th[i] * stratified_2_means[i] for i in range(N+1)])
    ci = compute_ci(stratified_2, 0.95, n_th, runs)
    est_2.append(res.total_mean)
    est_2_ci.append(res.ci_total_mean)
    est_2_strat.append(est)
    est_2_strat_ci.append(ci)
    print(f'Prob: {p}, est: {est }+-{ci} expected: {res.total_mean}+-{res.ci_total_mean}')

f, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.errorbar(
    probs,
    est_2,
    yerr=est_2_ci,
    label="base simulation",
    linestyle="dotted",
    marker="o",
    markersize=2,
)
ax.errorbar(
    probs,
    est_2_strat,
    yerr=est_2_strat_ci,
    label=" post stratification",
    linestyle="dotted",
    marker="o",
    markersize=2,
)
ax.plot(p_axis, d_zero_msg_2_expected_axis, label="theoretical")
ax.set_title("Comparison of theoretical, simulated and post stratified results for r=2, N=2")
ax.xaxis.set_label_text("p")
ax.yaxis.set_label_text("p no messages reached D") 
ax.legend()

r = 5
N = 5

est_5 = []
est_5_ci = []
est_5_strat = []
est_5_strat_ci = []

for p in probs:
    stratified_5 = []
    res = multiple_sim(r, N, p, runs, extended=True)

    binom = stats.binom(N, 1-p)
    p_th = binom.pmf(range(N+1))
    n_th = p_th*runs
    # print(f'p_th: {p_th}')

    for i in range(N+1):
        stratified_5.append(res.results[res.reached_layer_one == i])
    
    p_est = [len(stratified_5[i])/runs for i in range(N+1)]
    p_est = np.array(p_est)
    # print(f'p: {p_est}')

    stratified_5_means = [np.mean(stratified_5[i]) for i in range(N+1)]
    est = 1/runs * np.sum([n_th[i] * stratified_5_means[i] for i in range(N+1)])
    ci = compute_ci(stratified_5, 0.95, n_th, runs)
    est_5.append(res.total_mean)
    est_5_ci.append(res.ci_total_mean)
    est_5_strat.append(est)
    est_5_strat_ci.append(ci)
    print(f'Prob: {p}, est: {est }+-{ci} expected: {res.total_mean}+-{res.ci_total_mean}')

f, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.errorbar(
    probs,
    est_5,
    yerr=est_5_ci,
    label="base simulation",
    linestyle="dotted",
    marker="o",
    markersize=2,
)
ax.errorbar(
    probs,
    est_5_strat,
    yerr=est_5_strat_ci,
    label="post stratification",
    linestyle="dotted",
    marker="o",
    markersize=2,
)
ax.plot(p_axis, d_zero_msg_5_expected_axis, label="theoretical")
ax.set_title("Comparison of theoretical, simulated and post stratified results for r=5, N=5")
ax.xaxis.set_label_text("p")
ax.yaxis.set_label_text("p no messages reached D")
ax.legend()
plt.show()






