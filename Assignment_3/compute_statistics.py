import numpy as np
import matplotlib.pyplot as plt
import pandas.plotting as pdplt
import scipy.stats as stats
from utils.packet import Packet
from simulation_loop import simulation_loop
import pandas as pd

# Set simulation parameters and run simulation
l = 1.5
mu = 2.5
rho = l / mu
simulation_time = 2000
gen = np.random.default_rng(seed=41)
packets, queue_occupation = simulation_loop(simulation_time, l, mu, gen)

# Plot autocorrelation to find the initialization bias cutoff
pdplt.autocorrelation_plot(packets["waiting_time"])

f, ax = plt.subplots(4, figsize=(10, 20))

# Check if arrivals are uniformly distributed
x = np.linspace(0, simulation_time)
ax[0].hist(packets["arrival_time"], bins="auto", density=True, label="Arrival times")
ax[0].plot(x, stats.uniform.pdf(x, 0, simulation_time), label="Uniform distribution")
ax[0].set_title("Arrival distribution")
ax[0].legend()

# Check if service times are exponentially distributed both through a histogram and a Kolmogorov-Smirnoff test
x = np.linspace(0, 3)
service_times = packets["departure_time"] - packets["service_time"]
exp = stats.expon(scale=1 / mu)
ax[1].hist(service_times, bins="auto", density=True, label="Service times")
ax[1].plot(x, exp.pdf(x), label="Exponential distribution")
ax[1].set_title("Service distribution")
ax[1].legend()
test_exp = stats.kstest(
    service_times,
    stats.expon.cdf,
    args=(np.mean(service_times), 1 / mu),
)
print(test_exp)

# Plot the waiting times (should change based on rho)
ax[2].hist(packets["waiting_time"], bins="auto", density=True, label="Waiting times")
ax[2].set_title("Waiting time distribution")
ax[2].legend()

# For now as a first approximation statistics are computed on the entire run
packets_queue = (
    queue_occupation["total_packets"].values[:-1000]
    * queue_occupation["width"].values[:-1000]
)

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

# Check if average number of packets in the system is equal to the theoretical value
avg_packets_sim = np.sum(packets_queue) / total_width
ci_amplitude = 1.96 * np.std(packets_queue) / np.sqrt(len(packets_queue))
print(f"Average number of packets in the system (theory): {avg_packets_theory}")
print(
    f"Average number of packets in the system (simulation): {avg_packets_sim} +- {ci_amplitude}"
)

x = np.linspace(0, simulation_time)
ax[3].plot(
    queue_occupation["time"],
    queue_occupation["total_packets"],
    label="Packets in queue",
)
ax[3].plot(x, np.ones(len(x)) * avg_packets_theory, label="Theoretical average")
ax[3].plot(x, np.ones(len(x)) * avg_packets_sim, label="Simulation average")
ax[3].set_title("Queue occupation")
ax[3].legend()

plt.show()
