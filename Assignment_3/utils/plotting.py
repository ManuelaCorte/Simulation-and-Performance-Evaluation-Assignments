import matplotlib.pyplot as plt
import pandas.plotting as pdplt
import scipy.stats as stats
import numpy as np
import pandas as pd

# Plots the distribution of the arrival times and compares it to a uniform distribution
# Plots the distribution of the service times and compares it to an exponential distribution
class Plotting:
    def __init__(self, l, mu, packets, queue_occupation):
        self.l = l
        self.mu = mu
        self.packets = packets
        self.queue_occupation = queue_occupation
        self.rho = l / mu

    def plot_preliminary_functions(self):
        f, ax = plt.subplots(2, figsize=(10, 20))
        n = len(self.packets)
        # Check if arrivals are uniformly distributed
        x = np.linspace(0, n)
        ax[0].hist(self.packets["arrival_time"], bins="auto", density=True, label="Arrival times")
        ax[0].plot(x, stats.uniform.pdf(x, 0, n), label="Uniform distribution")
        ax[0].set_title("Arrival distribution")
        ax[0].legend()

        # Check if service times are exponentially distributed both through a histogram and a Kolmogorov-Smirnoff test
        x = np.linspace(0, 3)
        exp = stats.expon(scale=1 / self.mu)
        ax[1].hist(self.packets['server_time'], bins="auto", density=True, label="Service times")
        ax[1].plot(x, exp.pdf(x), label="Exponential distribution")
        ax[1].set_title("Service distribution")
        ax[1].legend()
        test_exp = stats.kstest(
            self.packets['server_time'],
            stats.expon.cdf,
            args=(np.mean(self.packets['server_time']), 1 / self.mu),
        )
        print(test_exp)

    def plot_waiting_times_distribution(self):
        f, ax = plt.subplots(1, figsize=(10, 20))
        ax.hist(self.packets["waiting_time"], bins="auto", density=True, label="Waiting times")
        ax.set_title("Waiting time distribution")
        ax.legend()

    def plot_queue_occupation(self):
        f, ax = plt.subplots(1, figsize=(10, 20))
        n = len(self.packets)
        x = np.linspace(0, n)
        ax.plot(
            self.queue_occupation["time"],
            self.queue_occupation["total_packets"],
            label="Packets in queue",
        )
        ax.set_title("Queue occupation")
        ax.legend()

    def plot_auto_correlation(self):
        f, ax = plt.subplots(1, figsize=(10, 20))
        pdplt.autocorrelation_plot(self.packets["waiting_time"])
        ax.set_title("Autocorrelation of waiting times")