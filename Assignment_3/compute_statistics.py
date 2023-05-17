import numpy as np
import matplotlib.pyplot as plt
from simulation_loop import simulation_loop
from utils.plotting import Plotting
from utils.stats import Statistics
from batch_means import compute_batch_means_statistics
from utils.SchedulingFunction import SchedulingFunction
import pandas as pd
import argparse
from pprint import pprint
from utils.compute_theoretical_statistics import compute_theoretical_statistics

# To speed up development we load the data from csv files instead of running the simulation
parser = argparse.ArgumentParser()
parser.add_argument(
    "--csv",
    action="store_true",
    help="Instead of running the simulation, load the data from a csv file",
)

# setting simulation parameters
l = 1.5
mu = 2
n_servers = 2
simulation_time = 100
# > 999 is considered infinite
max_queue_elements = 1000
gen = np.random.default_rng(seed=41)
scheduling = SchedulingFunction.LeastFull
args = parser.parse_args()

(
    rho, 
    avg_packets_in_system_th, 
    avg_waiting_time_th, 
    avg_response_time_th, 
    avg_queue_length_th
) = compute_theoretical_statistics(l, mu, n_servers, max_queue_elements)

if args.csv:
    print("Loading data from csv files")
    packets = pd.read_csv("packets_avg.csv")
    queue_occupation = pd.read_csv("queue_occupation_avg.csv")
    discarded_packets = pd.read_csv("discarded_packets_avg.csv")
else:
    print("Running simulation")
    packets, queue_occupation, discarded_packets = simulation_loop(simulation_time, l, mu, gen, n_servers, max_queue_elements, scheduling)


plot_util = Plotting(l, mu, n_servers, max_queue_elements , simulation_time, packets, queue_occupation)

# Plot distribution of arrival times and service times just to check they follow theoretical distributions
plot_util.plot_preliminary_functions()

# Peak of waiting times should move to the right the closer rho is to 1
plot_util.plot_waiting_times_distribution()

# Plot autocorrelation to decide batch size for batch means
# plot_util.plot_auto_correlation(Statistics.WAITING_TIME)
# plot_util.plot_auto_correlation(Statistics.RESPONSE_TIME)

total_width = np.sum(queue_occupation["width"])
number_of_packets = len(packets)

avg_packets_in_system_sim = (
    np.sum(queue_occupation["total_packets"] * queue_occupation["width"]) / total_width
)

utilization = (
    queue_occupation.loc[queue_occupation["total_packets"] != 0]["width"].sum()
    / total_width
)

(
    grand_mean_waiting_time,
    ci_amplitude_waiting_time,
    batch_means_waiting_time,
    intervals_waiting_time,
) = compute_batch_means_statistics(Statistics.WAITING_TIME, packets, 6000, 20000, 0.95)

# Techinically we should check that the batch size and the initialization bias is the same observed for the waiting times
# but the MM1 queue is simple enough that we assume it is the same
(
    grand_mean_response_time,
    ci_amplitude_response_time,
    batch_means_response_time,
    intervals_response_time,
) = compute_batch_means_statistics(Statistics.RESPONSE_TIME, packets, 6000, 20000, 0.95)


# Check if the time the system is used is equal to the theoretical value rho
print(f"Occupation: {utilization}, theoretical: {rho / n_servers}")
print(
    f"""Average number of packets in the system (theory): {avg_packets_in_system_th} \t
        Average number of packets in the system (simulation): {avg_packets_in_system_sim}"""
)

# Check if average time in the system is equal to the theoretical value using batch means
print(
    f"""Average response time (theory): {avg_response_time_th} \t
      Average response time (simulation): {grand_mean_response_time} +- {ci_amplitude_response_time}"""
)

# Check if average time waiting is equal to the theoretical value using batch means
print(
    f"""Average waiting time (theory): {avg_waiting_time_th} \t
        Average waiting time (simulation): {grand_mean_waiting_time} +- {ci_amplitude_waiting_time}"""
)

plot_util.plot_queue_occupation(avg_packets_in_system_sim)

plot_util.plot_utilization(n_servers)

plot_util.plot_batch_means(
    batch_means_waiting_time, intervals_waiting_time, Statistics.WAITING_TIME
)

plot_util.plot_batch_means(
    batch_means_response_time, intervals_response_time, Statistics.RESPONSE_TIME
)

plot_util.plot_servers_per_policy(scheduling)


plt.show()
