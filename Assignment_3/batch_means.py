import numpy as np

# We remove the warmup period --> batches are stationary
# We take batches double the size of the autocorrelation time --> batches means are independent
# We have enough batches that the means are normally distributed because of the CLT
def compute_batch_means_statistics(packets, queue_occupation, batch_size, warmup_time):
    packets = packets.loc[packets["arrival_time"] > warmup_time]
    queue_occupation = queue_occupation.loc[queue_occupation["time"] > warmup_time]

    # Compute the number of batches
    number_of_batches = int(len(packets) / batch_size)
    print(number_of_batches)

    # Compute batches
    batches = [packets[i * batch_size : (i + 1) * batch_size]['waiting_time'] for i in range(number_of_batches)]
    
    # Compute batches means
    batch_means = [
        np.mean(batch) for batch in batches]

    ci_amps = [1.96 * np.std(batch) / np.sqrt(batch_size) for batch in batches]
    
    # Compute grand mean
    grand_mean = np.mean(batch_means)

    # Compute variance of batch means
    var = (
        1
        / (number_of_batches - 1)
        * np.sum([(batch_means[i] - grand_mean) ** 2 for i in range(number_of_batches)])
    )

    ci_amplitude = 1.96 * np.sqrt(var / number_of_batches)

    return grand_mean, ci_amplitude, batch_means, ci_amps


def compute_overlapping_batch_means_statistics(
    packets, queue_occupation, batch_size, warmup_time
):
    pass
