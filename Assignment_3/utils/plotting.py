import matplotlib.pyplot as plt
import pandas.plotting as pdplt
import scipy.stats as stats
import numpy as np
import pandas as pd
from utils.stats import Statistics


# Plots the distribution of the arrival times and compares it to a uniform distribution
# Plots the distribution of the service times and compares it to an exponential distribution
class Plotting:
    def __init__(self, l, mu, simulation_time, packets, queue_occupation):
        self.l = l
        self.mu = mu
        self.simulation_time = simulation_time
        self.packets = packets
        self.queue_occupation = queue_occupation
        self.rho = l / mu

    def plot_preliminary_functions(self):
        f, ax = plt.subplots(2, figsize=(10, 20))
        # Check if arrivals are uniformly distributed
        x = np.linspace(0, self.simulation_time)
        ax[0].hist(
            self.packets["arrival_time"],
            bins="auto",
            density=True,
            label="Arrival times",
        )
        ax[0].plot(
            x,
            stats.uniform.pdf(x, 0, self.simulation_time),
            label="Uniform distribution",
        )
        ax[0].set_title("Arrival distribution")
        ax[0].legend()

        # Check if service times are exponentially distributed both through a histogram and a Kolmogorov-Smirnoff test
        x = np.linspace(0, 3)
        exp = stats.expon(scale=1 / self.mu)
        ax[1].hist(
            self.packets["server_time"],
            bins="auto",
            density=True,
            label="Service times",
        )
        ax[1].plot(x, exp.pdf(x), label="Exponential distribution")
        ax[1].set_title("Service distribution")
        ax[1].legend()
        test_exp = stats.kstest(
            self.packets["server_time"],
            stats.expon.cdf,
            args=(np.mean(self.packets["server_time"]), 1 / self.mu),
        )
        print(test_exp)

    def plot_waiting_times_distribution(self):
        f, ax = plt.subplots(1, figsize=(10, 20))
        ax.hist(
            self.packets["waiting_time"],
            bins="auto",
            density=True,
            label="Waiting times",
        )
        ax.set_title("Waiting time distribution")
        ax.legend()

    def plot_queue_occupation(self, sim_mean):
        f, ax = plt.subplots(1, figsize=(10, 20))
        ax.step(
            self.queue_occupation["width"].cumsum(),
            self.queue_occupation["total_packets"],
            label="Packets in queue",
        )
        ax.axhline(self.rho / (1 - self.rho), label="Theoretical mean", color="b")
        ax.axhline(sim_mean, label="Simulation mean", color="r")

        ax.set_title("Queue occupation")
        ax.legend()

    def plot_utilization(self, n_servers):
        f, ax = plt.subplots(1, figsize=(10, 20))
        avg = (
            self.queue_occupation[self.queue_occupation["total_packets"] != 0][
                "width"
            ].cumsum()
            / self.queue_occupation["width"].cumsum()
        )
        ax.plot(avg, label="Utilization", color="b")
        ax.axhline(self.rho / n_servers, label="Theoretical value", color="r")
        ax.set_title("Utilization")
        ax.legend()

    def plot_auto_correlation(self, type):
        f, ax = plt.subplots(1, figsize=(10, 20))
        match type:
            case Statistics.RESPONSE_TIME:
                pdplt.autocorrelation_plot(self.packets["total_time"])
                ax.set_title("Autocorrelation of response times")
            case Statistics.WAITING_TIME:
                pdplt.autocorrelation_plot(self.packets["waiting_time"])
                ax.set_title("Autocorrelation of waiting times")
            case _:
                raise ValueError("Invalid type")

    def plot_confidence_interval(
        self, x, mean, ci, color="#2187bb", horizontal_line_width=0.25
    ):
        left = x - horizontal_line_width / 2
        top = mean - ci
        right = x + horizontal_line_width / 2
        bottom = mean + ci
        plt.plot([x, x], [top, bottom], color=color)
        plt.plot([left, right], [top, top], color=color)
        plt.plot([left, right], [bottom, bottom], color=color)
        plt.plot(x, mean, "o", color="#f44336")

    def plot_batch_means(self, batch_means, intervals, type):
        f, ax = plt.subplots(1, figsize=(10, 20))
        for i in range(len(batch_means)):
            self.plot_confidence_interval(i + 1, batch_means[i], intervals[i])
        match type:
            case Statistics.WAITING_TIME:
                ax.axhline(
                    self.rho / (self.mu - self.l), color="r", label="Theoretical mean"
                )
                ax.set_title("Batch means of waiting times")
            case Statistics.RESPONSE_TIME:
                ax.axhline(1 / (self.mu - self.l), color="r", label="Theoretical mean")
                ax.set_title("Batch means of response times")
        ax.legend()
