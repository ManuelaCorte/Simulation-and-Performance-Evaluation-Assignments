import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from utils.packet import Packet
from simulation_loop import simulation_loop
import pandas as pd

l= 2.0
mu = 2.5
simulation_time = 1000
packets = simulation_loop(simulation_time, l = l, mu = mu, seed = 41)
arrival_times = [packet.arrival_time for packet in packets.values()][:-1] # check if uniformly distributed
waiting_times = [packet.compute_waiting_time() for packet in packets.values()][:-1]
service_times = [packet.compute_server_occupation_time() for packet in packets.values()][:-1] # check if exponential of parameter mu
# df = pd.DataFrame.from_records([packet.__dict__ for packet in packets.values()])
# print(df.head())

f, ax = plt.subplots(3, figsize = (10, 10))
ax[0].hist(arrival_times, bins = 'auto', density = True, label = 'Arrival times')
x = np.linspace(0, simulation_time)
ax[0].plot(x, stats.uniform.pdf(x, 0, simulation_time), label = 'Uniform distribution')
# ax.plot(np.linspace(0, 10, 100), stats.uniform.pdf(np.linspace(0, 10, 100), 0, 10), label = 'Uniform distribution')
ax[0].set_title('Arrival distribution')

# f, ax = plt.subplots(1)
ax[1].hist(service_times, bins = 'auto', density = True, label = 'Service times')
exp = stats.expon(scale = 1/mu)
x = np.linspace(0, 3)
ax[1].plot(x, exp.pdf(x), label = 'Exponential distribution')
ax[1].set_title('Service distribution')

ax[2].hist(waiting_times, bins = 'auto', density = True, label = 'Waiting times')
ax[2].set_title('Waiting time distribution')
print(np.min(waiting_times), np.max(waiting_times))
# test_unif = stats.kstest(arrival_times, 'uniform', )
# test_exp = stats.kstest(service_times, 'expon',)
# print(test_unif)
# print(test_exp)
plt.show()
