import numpy as np
import matplotlib.pyplot as plt
import pandas.plotting as pdplt
import scipy.stats as stats
from utils.packet import Packet
from simulation_loop import simulation_loop
import pandas as pd
import scipy.signal as signal

l = 1.5
mu = 2.5
rho = l / mu
simulation_time = 7000
number_of_runs = 5
gen = np.random.default_rng(seed=41)
simulations = [simulation_loop(simulation_time, l, mu, gen) for i in range(number_of_runs)]

waiting_times = [simulations[i][0]['waiting_time'] for i in range(number_of_runs)]

n = min([len(x) for x in waiting_times])
print(n)
f, ax = plt.subplots(1) 
x = np.linspace(0, 100000, 1)
for i in range(number_of_runs):
    
    # avg = waiting_times[i].cumsum() / (np.arange(len(waiting_times[i])) + 1)
    ax.plot(waiting_times[i].expanding().mean(), label=f"Waiting time run {i}")
    ax.plot(np.ones(len(x)) * rho**2/(l*(1-rho)), label="Theoretical value")
plt.show()
