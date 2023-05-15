import numpy as np
import matplotlib.pyplot as plt
import pandas.plotting as pdplt
import scipy.stats as stats
from utils.packet import Packet
from simulation_loop import simulation_loop
import pandas as pd
import scipy.signal as signal
import argparse

# Set simulation parameters and run simulation
parser = argparse.ArgumentParser()
parser.add_argument('--csv', action='store_true', help='Instead of running the simulation, load the data from a csv file')


l = 1.5
mu = 2.5
rho = l / mu
simulation_time = 5000
number_of_runs = 1
gen = np.random.default_rng(seed=41)
args = parser.parse_args()

if args.csv:
    print("Loading data from csv files")
    packets = pd.read_csv('packets.csv')
    queue_occupation = pd.read_csv('queue_occupation.csv')
else:
    print("Running simulation")
    packets, queue_occupation = simulation_loop(simulation_time, l, mu, gen)

packets, queue_occupation = simulation_loop(simulation_time, l, mu, gen)

f, ax = plt.subplots(4, figsize=(10, 20))

# Check if arrivals are uniformly distributed
x = np.linspace(0, simulation_time)
ax[0].hist(packets["arrival_time"], bins="auto", density=True, label="Arrival times")
ax[0].plot(x, stats.uniform.pdf(x, 0, simulation_time), label="Uniform distribution")
ax[0].set_title("Arrival distribution")
ax[0].legend()

# Check if service times are exponentially distributed both through a histogram and a Kolmogorov-Smirnoff test
x = np.linspace(0, 3)
exp = stats.expon(scale=1 / mu)
ax[1].hist(packets['server_time'], bins="auto", density=True, label="Service times")
ax[1].plot(x, exp.pdf(x), label="Exponential distribution")
ax[1].set_title("Service distribution")
ax[1].legend()
test_exp = stats.kstest(
    packets['server_time'],
    stats.expon.cdf,
    args=(np.mean(packets['server_time']), 1 / mu),
)
print(test_exp)

# Plot the waiting times (should change based on rho)
ax[2].hist(packets["waiting_time"], bins="auto", density=True, label="Waiting times")
ax[2].set_title("Waiting time distribution")
ax[2].legend()

x = np.linspace(0, simulation_time)
ax[3].plot(
    queue_occupation["time"],
    queue_occupation["total_packets"],
    label="Packets in queue",
)
ax[3].set_title("Queue occupation")
ax[3].legend()

f, ax = plt.subplots(1)
pdplt.autocorrelation_plot(packets["waiting_time"], ax=ax)



# Compute "fixed" statistics
avg_packets_theory = rho / (1 - rho)
total_width = np.sum(queue_occupation["width"])
avg_time_in_system_sim = np.sum(packets["total_time"]) / len(packets)
avg_time_in_system_theory = 1 / (mu - l)
avg_time_waiting_sim = np.sum(packets["waiting_time"]) / len(packets)
avg_time_waiting_theory = rho / (mu - l)
utilization = (
    queue_occupation.loc[queue_occupation["packets_in_queue"] != 0]["width"].sum()
    / total_width
)


# Check if the time the system id empty is equal to the theoretical value rho
print(f"Occupation: {utilization}, theoretical: {rho}")

# Check if average time in the system is equal to the theoretical value
print(f"Average time in the system (theory): {avg_time_in_system_theory}")
print(f"Average time in the system (simulation): {avg_time_in_system_sim}")

# Check if average time waiting is equal to the theoretical value
print(f"Average time waiting (theory): {avg_time_waiting_theory}")
print(f"Average time waiting (simulation): {avg_time_waiting_sim}")

avg_packets_sim = np.sum(packets['waiting_time']) / len(packets)
avg_packets_theory = rho / (1 - rho)
print(f"Average number of packets in the system (theory): {avg_packets_theory}")
print(
    f"Average number of packets in the system (simulation): {avg_packets_sim}"
)

plt.show()
