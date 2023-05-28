import numpy as np
import matplotlib.pyplot as plt
from fn.compute_ci import compute_ci


def compute_pi_base(N: int, gen) -> None:
    x_coordinates = gen.uniform(-1, 1, N)
    y_coordinates = gen.uniform(-1, 1, N)

    distances = x_coordinates**2 + y_coordinates**2 <= 1
    mean = np.mean(distances)
    ci = compute_ci(distances, 0.95)
    print(f"Mean: {4*mean} +-{ci}, CI size: {2*ci}")

    f, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.scatter(x_coordinates[distances], y_coordinates[distances], color="blue", s=1)
    ax.scatter(x_coordinates[~distances], y_coordinates[~distances], color="red", s=1)
    circle = plt.Circle((0, 0), 1, color="black", fill=False, linewidth=2)
    ax.add_patch(circle)
    ax.set_title("Estimation of pi")
    plt.show()


def compute_pi_conditioning_antithetic(N, gen) -> None:
    uniform_samples = gen.uniform(0, 1, N)
    sample = 0.5 * (
        np.sqrt(1 - uniform_samples**2) + np.sqrt(1 - (1 - uniform_samples) ** 2)
    )
    ci = compute_ci(sample, 0.95)
    print(f"Mean: {4*np.mean(sample)} +-{ci}, CI size: {2*ci}")


def compute_pi_strafied(N, gen) -> None:
    uniform_samples = gen.uniform(0, 1, N)
    indexes = np.arange(0, N)
    samples = np.sqrt(1 - ((uniform_samples + indexes - 1) / N) ** 2) + np.sqrt(
        1 - ((indexes - uniform_samples) / N) ** 2
    )
    ci = compute_ci(samples, 0.95)
    print(f"Mean: {2*np.mean(samples)} +-{ci}, CI size: {2*ci}")


N = 1000000  # number of points
gen = np.random.default_rng(seed=31415)
ci_level = 0.95
number_of_simulations = 1

print(f"Theory value: {np.pi}\n")

compute_pi_base(N, gen)
compute_pi_conditioning_antithetic(N, gen)
compute_pi_strafied(N, gen)
