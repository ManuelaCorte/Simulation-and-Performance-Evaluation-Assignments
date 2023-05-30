import numpy as np
import matplotlib.pyplot as plt
from fn.compute_ci import compute_ci

def plot_histogram(data, title):
    f, ax = plt.subplots(1, 1, figsize=(10, 10))
    counts, _, _ = ax.hist(data, bins='auto', density=True, label='Samples')
    ax.set_title(title)
    ax.vlines(np.pi, ymin=0, ymax=max(counts), linewidth=2,color="red", label='Pi')
    ax.legend()

def compute_pi_base(N: int, gen, num_sim) -> None:
    pi = np.zeros(num_sim)
    for i in range(num_sim):
        x_coordinates = gen.uniform(-1, 1, N)
        y_coordinates = gen.uniform(-1, 1, N)

        distances = x_coordinates**2 + y_coordinates**2 <= 1
        pi[i] = np.mean(distances)

        if i == 0:
            f, ax = plt.subplots(1, 1, figsize=(10, 10))
            ax.scatter(x_coordinates[distances], y_coordinates[distances], color="blue", s=1)
            ax.scatter(x_coordinates[~distances], y_coordinates[~distances], color="red", s=1)
            circle = plt.Circle((0, 0), 1, color="black", fill=False, linewidth=2)
            ax.add_patch(circle)
            ax.set_title("Estimation of pi")

    mean = 4*np.mean(pi)
    ci = compute_ci(pi, 0.95)
    print(f"Mean: {mean} +-{ci}, CI size: {2*ci}")


def compute_pi_conditioning_antithetic(N, gen, num_sim) -> None:
    pi = np.zeros(num_sim)
    for i in range(num_sim):
        uniform_samples = gen.uniform(0, 1, N)
        sample = (
            np.sqrt(1 - uniform_samples**2) + np.sqrt(1 - (1 - uniform_samples) ** 2)
        )
        pi[i] = np.mean(sample)
    mean = 2*np.mean(pi)
    ci = compute_ci(pi, 0.95)
    print(f"Mean: {mean} +-{ci}, CI size: {2*ci}")
    # plot_histogram(2*pi, "Estimation of pi antithetic")


def compute_pi_strafied(N, gen, num_sim) -> None:
    pi = np.zeros(num_sim)
    for i in range(num_sim):
        uniform_samples = gen.uniform(0, 1, N)
        indexes = np.arange(1, N+1)
        samples = np.sqrt(1 - ((uniform_samples + indexes - 1) / N) ** 2) + np.sqrt(
            1 - ((indexes - uniform_samples) / N) ** 2
        )
        pi[i] = np.mean(samples)
    mean = 2*np.mean(pi)
    ci = compute_ci(pi, 0.95)
    print(f"Mean: {mean}+-{ci}, CI size: {2*ci}")
    # plot_histogram(2*pi, "Estimation of pi strafied")


N = 1000000  # number of points
gen = np.random.default_rng(seed=31415)
ci_level = 0.95
number_of_simulation = 100
print(f"Theory value: {np.pi}\n")

compute_pi_base(N, gen, number_of_simulation)
compute_pi_conditioning_antithetic(N, gen, number_of_simulation)
compute_pi_strafied(N, gen, number_of_simulation)

plt.show()
