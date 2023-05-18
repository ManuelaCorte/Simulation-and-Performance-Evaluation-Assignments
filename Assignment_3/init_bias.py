import numpy as np
import matplotlib.pyplot as plt
from simulation_loop import simulation_loop
from functools import reduce
import argparse

l = 1.5
mu = 2.5
rho = l / mu
simulation_time = 30000
number_of_runs = 10
gen = np.random.default_rng(seed=41)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--wt",
    action="store_true",
    help="Compute initialization bias for waiting time",
)
parser.add_argument(
    "--rt", action="store_true", help="Compute initialization bias for response time"
)
args = parser.parse_args()

simulations = [
    simulation_loop(simulation_time, l, mu, gen) for i in range(number_of_runs)
]

vars = []
if args.wt:
    print("Computing initialization bias for waiting time")
    vars = [simulations[i][0]["waiting_time"] for i in range(number_of_runs)]
elif args.rt:
    print("Computing initialization bias for response time")
    vars = [simulations[i][0]["total_time"] for i in range(number_of_runs)]
else:
    print("Please specify --wt or --rt")
    exit()

df = reduce(lambda a, b: a.add(b, fill_value=0), vars)
f, ax = plt.subplots(1)
if args.wt:
    ax.set_title("Initialization bias for waiting time")
    for i in range(number_of_runs):
        ax.plot(vars[i].expanding().mean(), label=f"Waiting time run {i}")
    ax.plot(
        df.expanding().mean() / number_of_runs, label="Average waiting time across runs", linewidth=3, color="red")
    ax.axhline(rho / (mu - l), label="Theoretical value")
elif args.rt:
    ax.set_title("Initialization bias for response time")
    for i in range(number_of_runs):
        ax.plot(vars[i].expanding().mean(), label=f"Response time run {i}")
    ax.plot(
        df.expanding().mean() / number_of_runs, label="Average response time across runs", linewidth=3, color="red"
    )
    ax.axhline(1 / (mu - l), label="Theoretical value")
ax.legend()

# By looking at the plots we can cut the first 10000 packets for average load
# For rho closer to 1 the warmup time should be much longer
plt.show()
