import numpy as np
import matplotlib.pyplot as plt
import pandas.plotting as pdplt
import scipy.stats as stats
from simulation_loop import simulation_loop
from simulation_loop_multiple_servers import simulation_loop_multiple_servers
from utils.plotting import Plotting
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

plot_util = Plotting(l, mu, packets, queue_occupation)

plot_util.plot_preliminary_functions()

plot_util.plot_waiting_times_distribution()

plot_util.plot_queue_occupation()

plot_util.plot_auto_correlation()

plt.show()


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
