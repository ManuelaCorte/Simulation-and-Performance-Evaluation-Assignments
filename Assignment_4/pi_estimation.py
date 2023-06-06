from typing import Callable, List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from fn.compute_ci import compute_ci


def plot_histogram(data: List[float] | np.ndarray[float], title: str) -> None:
    f, ax = plt.subplots(1, 1, figsize=(10, 10))
    counts, bins, _ = ax.hist(data, bins="auto", label="Samples")
    # print(bins[0], bins[-1])
    ax.set_title(title)
    # ax.ticklabel_format(axis="both", style="plain", scilimits=(0,0))
    ax.vlines(np.pi, ymin=0, ymax=max(counts), linewidth=2, color="red", label="Pi")
    ax.legend()


def compute_pi_base(N: int, num_sim: int, plot=False) -> Tuple[float, float]:
    gen = np.random.default_rng(seed=314)
    pi = np.zeros(num_sim)
    for i in range(num_sim):
        x_coordinates = gen.uniform(-1, 1, N)
        y_coordinates = gen.uniform(-1, 1, N)

        distances = x_coordinates**2 + y_coordinates**2 <= 1
        pi[i] = np.mean(distances)

        if i == 0 and plot:
            f, ax = plt.subplots(1, 1, figsize=(10, 10))
            ax.scatter(
                x_coordinates[distances], y_coordinates[distances], color="blue", s=1
            )
            ax.scatter(
                x_coordinates[~distances], y_coordinates[~distances], color="red", s=1
            )
            circle = plt.Circle((0, 0), 1, color="black", fill=False, linewidth=2)
            ax.add_patch(circle)
            ax.set_title("Estimation of pi")
    if plot:
        plot_histogram(4 * distances, "Distribution on samples for pi base estimation")
        plot_histogram(4 * pi, "Estimation of pi base")
    mean = 4 * np.mean(pi)
    ci = compute_ci(pi, 0.95)
    return mean, ci


def compute_pi_conditioning_antithetic(
    N: int, num_sim: int, plot=False
) -> Tuple[float, float]:
    gen = np.random.default_rng(seed=31415)
    pi = np.zeros(num_sim)
    for i in range(num_sim):
        uniform_samples = gen.uniform(0, 1, N)
        samples = np.sqrt(1 - uniform_samples**2) + np.sqrt(
            1 - (1 - uniform_samples) ** 2
        )
        pi[i] = np.mean(samples)
    if plot:
        plot_histogram(2 * samples, "Distribution of samples for pi antithetic")
        plot_histogram(2 * pi, "Estimation of pi antithetic")
    mean = 2 * np.mean(pi)
    ci = compute_ci(pi, 0.95)
    return mean, ci


def compute_pi_strafied(N: int, num_sim: int, plot=False) -> Tuple[float, float]:
    gen = np.random.default_rng(seed=3141529)
    pi = np.zeros(num_sim)
    for i in range(num_sim):
        uniform_samples = gen.uniform(0, 1, N)
        indexes = np.arange(1, N + 1)
        samples = np.sqrt(1 - ((uniform_samples + indexes - 1) / N) ** 2) + np.sqrt(
            1 - ((indexes - uniform_samples) / N) ** 2
        )
        pi[i] = np.mean(samples)
    if plot:
        plot_histogram(2 * samples, "Distribution of samples for pi strafied")
        plot_histogram(2 * pi, "Estimation of pi strafied")
    mean = 2 * np.mean(pi)
    ci = compute_ci(pi, 0.95)
    return mean, ci


# Run multiple full simulation with increasing number of points per simulation until the CI is small enough
def multiple_runs(
    N: int,
    increment: int,
    number_of_simulations: int,
    estimator: Callable[[int, int, bool], Tuple[float, float]],
) -> None:
    while True:
        print(f"Points: {N}")
        mean, ci = estimator(N, number_of_simulations)
        if 2 * ci < 1e-4:
            print(f"Mean: {mean}+-{ci}, CI size: {2*ci}")
            break
        N += increment


ci_level = 0.95
number_of_simulation = 100

# We start from different number of points based on the method to speed up the process
multiple_runs(2000000, 10000, number_of_simulation, compute_pi_base)
multiple_runs(150000, 1000, number_of_simulation, compute_pi_conditioning_antithetic)
multiple_runs(10, 1, number_of_simulation, compute_pi_strafied)

# Run a single simulation with a fixed number of points and plot the results
N = 100000  # number of points
number_of_simulation = 1000
print(f"Theory value: {np.pi}\n")

mean, ci = compute_pi_base(N, number_of_simulation, plot=True)
print(f"Mean: {mean}+-{ci}, CI size: {2*ci}")

mean, ci = compute_pi_conditioning_antithetic(N, number_of_simulation, plot=True)
print(f"Mean: {mean}+-{ci}, CI size: {2*ci}")

mean, ci = compute_pi_strafied(N, number_of_simulation, plot=True)
print(f"Mean: {mean}+-{ci}, CI size: {2*ci}")

plt.show()
