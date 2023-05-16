import numpy as np
import matplotlib.pyplot as plt
from simulation_loop import simulation_loop
from functools import reduce

l = 1.5
mu = 2.5
rho = l / mu
simulation_time = 500
number_of_runs = 5
gen = np.random.default_rng(seed=41)
simulations = [
    simulation_loop(simulation_time, l, mu, gen) for i in range(number_of_runs)
]

waiting_times = [simulations[i][0]["waiting_time"] for i in range(number_of_runs)]

n = min([len(x) for x in waiting_times])
print(n)
f, ax = plt.subplots(1)
for i in range(number_of_runs):
    # avg = waiting_times[i].cumsum() / (np.arange(len(waiting_times[i])) + 1)
    ax.plot(waiting_times[i].expanding().mean(), label=f"Waiting time run {i}")
    ax.axhline(rho / (mu - l), label="Theoretical value")

# Plot average between all runs
f, ax = plt.subplots(1)

df = reduce(lambda a, b: a.add(b, fill_value=0), waiting_times)
ax.plot(df.expanding().mean() / number_of_runs, label="Average waiting time")
ax.axhline(rho / (mu - l), label="Theoretical value")

# By looking at the plots we can cut the first 10000 packets for average load
# For rho closer to 1 the warmup time should be much longer
plt.show()
