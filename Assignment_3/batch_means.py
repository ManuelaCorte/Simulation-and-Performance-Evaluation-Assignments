import numpy as np
import scipy.stats as stats
from utils.stats import Statistics
import pandas.plotting as pdplt
import matplotlib.pyplot as plt

# We remove the warmup period --> batches are stationary
# We take batches double the size of the autocorrelation time --> batches means are independent
# We have enough batches that the means are normally distributed because of the CLT
def compute_batch_means_statistics(type, packets, batch_size, warmup_time, z):
    packets = packets.loc[packets["arrival_time"] > warmup_time]
    # queue_occupation = queue_occupation.loc[queue_occupation["time"] > warmup_time]

    # Compute batches
    match type:
        case Statistics.WAITING_TIME:
            batches = [
                packets[i * batch_size : (i + 1) * batch_size]["waiting_time"]
                for i in range(int(len(packets) / batch_size))
            ]
        case Statistics.RESPONSE_TIME:
            batches = [
                packets[i * batch_size : (i + 1) * batch_size]["total_time"]
                for i in range(int(len(packets) / batch_size))
            ]
        case _:
            raise ValueError("Invalid type")
    batches = batches[:-1]  # remove last batch that is smaller than the others

    # Compute number of batches
    number_of_batches = len(batches)
    print(f"Number of batches: {number_of_batches} of size {batch_size}")

    # Compute batches means
    batch_means = [np.mean(batch) for batch in batches]
    eta = stats.norm.ppf((1 + z) / 2) # We have enough batches to use the CLT
    ci_amps = [eta * np.std(batch) / np.sqrt(batch_size) for batch in batches]

    # This way we are checking whether the batches are independent one from the other
    f, ax = plt.subplots(1)
    pdplt.autocorrelation_plot(batch_means, ax=ax)

    # Compute grand mean
    grand_mean = np.mean(batch_means)

    # Compute variance of batch means
    var = (
        1
        / (number_of_batches - 1)
        * np.sum([(batch_mean - grand_mean) ** 2 for batch_mean in batch_means])
    )

    ci_amplitude = eta * np.sqrt(var / number_of_batches)

    return grand_mean, ci_amplitude, batch_means, ci_amps


