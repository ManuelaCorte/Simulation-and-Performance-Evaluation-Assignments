import numpy as np
import matplotlib.pyplot as plt
from simulation_loop import simulation_loop
from utils.plotting import Plotting
import pandas as pd
import argparse
from pprint import pprint


# To speed up development we load the data from csv files instead of running the simulation
parser = argparse.ArgumentParser()
parser.add_argument(
    "--csv",
    action="store_true",
    help="Instead of running the simulation, load the data from a csv file",
)

# setting simulation parameters
l = 1.5
mu = 2.5
simulation_time = 100000
gen = np.random.default_rng(seed=41)
args = parser.parse_args()

if args.csv:
    print("Loading data from csv files")
    packets = pd.read_csv("packets_avg.csv")
    queue_occupation = pd.read_csv("queue_occupation_avg.csv")
else:
    print("Running simulation")
    packets, queue_occupation = simulation_loop(simulation_time, l, mu, gen)


plot_util = Plotting(l, mu, simulation_time, packets, queue_occupation)

# Plot distribution of arrival times and service times just to check they follow theoretical distributions
plot_util.plot_preliminary_functions()

# Peak of waiting times should move to the right the closer rho is to 1
plot_util.plot_waiting_times_distribution()


# Plot autocorrelation to decide batch size for batch means
plot_util.plot_auto_correlation()


# Compute theory statistics
total_width = np.sum(queue_occupation["width"])
number_of_packets = len(packets)
rho = l / mu
avg_packets_in_system_th = rho / (1 - rho)
avg_response_time_th = 1 / (mu - l)  # Little's law
avg_waiting_time_th = rho / (mu - l)
avg_queue_length_th = 1 / (1 - rho)

avg_response_time_sim = np.sum(packets["total_time"]) / number_of_packets
ci_response_time = 1.96 * np.std(packets["total_time"]) / np.sqrt(number_of_packets)

avg_waiting_time_sim = np.sum(packets["waiting_time"]) / number_of_packets
ci_waiting_time = 1.96 * np.std(packets["waiting_time"]) / np.sqrt(number_of_packets)

avg_packets_in_system_sim = (
    np.sum(queue_occupation["total_packets"] * queue_occupation["width"]) / total_width
)
ci_packets_in_system = (
    1.96
    * np.std(queue_occupation["total_packets"] * queue_occupation["width"])
    / np.sqrt(total_width)
)
utilization = (
    queue_occupation.loc[queue_occupation["total_packets"] != 0]["width"].sum()
    / total_width
)


# Check if the time the system is used is equal to the theoretical value rho
print(f"Occupation: {utilization}, theoretical: {rho}")

# Check if average time in the system is equal to the theoretical value
print(
    f"""Average response time (theory): {avg_response_time_th} \t
      Average response time (simulation): {avg_response_time_sim} +- {ci_response_time}"""
)

# Check if average time waiting is equal to the theoretical value
print(
    f"""Average waiting time (theory): {avg_waiting_time_th} \t
        Average waiting time (simulation): {avg_waiting_time_sim} +- {ci_waiting_time}"""
)

print(
    f"""Average number of packets in the system (theory): {avg_packets_in_system_th} \t
        Average number of packets in the system (simulation): {avg_packets_in_system_sim} +- {ci_packets_in_system}"""
)

plot_util.plot_queue_occupation(avg_packets_in_system_sim)

plot_util.plot_utilization()
plt.show()
