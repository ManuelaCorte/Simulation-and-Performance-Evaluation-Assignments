import math

# https://en.wikipedia.org/wiki/M/M/c_queue#Stationary_analysis_2
def compute_pi_zero(rho, c, k):
        pi_zero = 0
        for j in range(c + 1):
            pi_zero = pi_zero + (rho ** j / math.factorial(j))
        extra_factor = 0
        for j in range(c+1, k+1):
            extra_factor = extra_factor + (rho/c) ** (j-c) 
        pi_zero = pi_zero + (rho ** c / math.factorial(c)) * extra_factor
        pi_zero = pi_zero ** -1
        return pi_zero

def compute_pi_k(rho, c, k, pi_zero):
        if k > 999:
            return 0
        if k <= c:
            return pi_zero * (rho ** k) / math.factorial(k)
        else:
            return pi_zero * (rho ** k) / ((c ** (k - c)) * math.factorial(c))

# Compute theory statistics
def compute_theoretical_statistics(l, mu, n_servers = 2, max_queue_elements = 1000):
    rho = l / mu
    c = n_servers
    k = max_queue_elements
    if rho / c >= 1:
        raise "rho / c >= 1"
    
    pi_zero = compute_pi_zero(rho, n_servers, k)

    # L
    avg_packets_in_system_th = rho + pi_zero * rho * ((rho * c) ** c) / (((1 - rho) ** 2) * math.factorial(c))

    # W_q
    avg_waiting_time_th = pi_zero * rho * ((rho * c) ** c) / (((1 - rho) ** 2) * math.factorial(c) * l)

    # W
    avg_response_time_th = 1 / mu + avg_waiting_time_th

    # lambda_a
    effective_arrival_wait = l * (1 - compute_pi_k(rho, c, k, pi_zero))

    # L_q
    avg_queue_length_th = effective_arrival_wait * avg_waiting_time_th

    return rho, avg_packets_in_system_th, avg_waiting_time_th, avg_response_time_th, avg_queue_length_th