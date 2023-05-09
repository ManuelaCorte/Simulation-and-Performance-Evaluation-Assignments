import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from utils.packet import Packet
from simulation_loop import simulation_loop
import pandas as pd

l = 2.0
mu = 2.5
simulation_time = 1000
gen = np.random.default_rng(seed=41)
packets, queue_occupation = simulation_loop(simulation_time, l, mu, gen)
# check if uniformly distributed
arrival_times = packets['arrival_time'][:-1]
waiting_times = packets['waiting_time'][:-1]
# check if exponential of parameter mu
service_times = packets ["departure_time"][:-1] - packets['service_time'][:-1]
# df = pd.DataFrame.from_records([packet.__dict__ for packet in packets.values()])
# print(df.head())

f, ax = plt.subplots(4, figsize=(10, 20))
ax[0].hist(arrival_times, bins="auto", density=True, label="Arrival times")
x = np.linspace(0, simulation_time)
ax[0].plot(x, stats.uniform.pdf(x, 0, simulation_time), label="Uniform distribution")
# ax.plot(np.linspace(0, 10, 100), stats.uniform.pdf(np.linspace(0, 10, 100), 0, 10), label = 'Uniform distribution')
ax[0].set_title("Arrival distribution")
ax[0].legend()

# f, ax = plt.subplots(1)
ax[1].hist(service_times, bins="auto", density=True, label="Service times")
exp = stats.expon(scale=1 / mu)
x = np.linspace(0, 3)
ax[1].plot(x, exp.pdf(x), label="Exponential distribution")
ax[1].set_title("Service distribution")
ax[1].legend()

ax[2].hist(waiting_times, bins="auto", density=True, label="Waiting times")
ax[2].set_title("Waiting time distribution")
ax[2].legend()
# print(np.min(waiting_times), np.max(waiting_times))
# test_unif = stats.kstest(arrival_times, 'uniform', )
# test_exp = stats.kstest(service_times, 'expon',)
# print(test_unif)
# print(test_exp)

# f, ax = plt.subplots(1)
ax[3].plot(queue_occupation['time'], queue_occupation['packets_in_queue'], label='Packets in queue')
ax[3].set_title("Queue occupation")
ax[3].legend()
plt.show()
