import math

# https://en.wikipedia.org/wiki/M/M/c_queue#Stationary_analysis_2
# http://dimacs.rutgers.edu/archive/Workshops/ASIEconEpi/Slides/Queuing_Theory_Equations.pdf
def compute_pi_zero(rho, c, k):
        pi_zero = 0
        # for j in range(c + 1):
        #     pi_zero = pi_zero + (rho ** j / math.factorial(j))
        # extra_factor = 0
        # for j in range(c+1, k+1):
        #     extra_factor = extra_factor + (rho/c) ** (j-c) 
        # pi_zero = pi_zero + (rho ** c / math.factorial(c)) * extra_factor
        # pi_zero = pi_zero ** -1
        for n in range(c):
            pi_zero = pi_zero + (rho ** n / math.factorial(n))
        pi_zero = pi_zero + (rho ** c / math.factorial(c)) * ((1-(rho/c)**(k-c+1)) / (1-rho/c))
        return pi_zero**(-1)

def compute_pi_n(n, rho, c, k, pi_zero):
        if k > 999:
            return 0
        if n <= c:
            return pi_zero * (rho ** n) / math.factorial(n)
        else:
            return pi_zero * (rho ** n) / ((c ** (n - c)) * math.factorial(c))

# Compute theory statistics
def compute_theoretical_statistics(l, mu, n_servers = 2, max_queue_elements = 1000):
    rho = l /  mu
    c = n_servers
    k = max_queue_elements
    if rho / c >= 1:
        raise "rho / c >= 1"
    
    pi_zero = compute_pi_zero(rho, n_servers, k)

    # # L
    # avg_packets_in_system_th = rho + pi_zero * rho * ((rho * c) ** c) / (((1 - rho) ** 2) * math.factorial(c))

    # # W_q
    # avg_waiting_time_th = pi_zero * rho * ((rho * c) ** c) / (((1 - rho) ** 2) * math.factorial(c) * l)

    # # W
    # avg_response_time_th = 1 / mu + avg_waiting_time_th

    # # lambda_a
    # effective_arrival_wait = l * (1 - compute_pi_k(rho, c, k, pi_zero))

    # # L_q
    # avg_queue_length_th = effective_arrival_wait * avg_waiting_time_th

    avg_queue_length_th = ((pi_zero*(rho**c)*(rho/c)) / (math.factorial(c)*(1-rho/c)**2)) * (1-(rho/c)**(k-c+1) - (1-rho/c)*(k-c+1)*(rho/c)**(k-c))

    factor = 0
    for n in range(c):
        factor = factor + ((c-n) * rho**n)/math.factorial(n)
    avg_packets_in_system_th = avg_queue_length_th + c - pi_zero*factor

    avg_response_time_th = avg_packets_in_system_th / (l*(1-compute_pi_n(k, rho, c, k, pi_zero)))

    avg_waiting_time_th= avg_response_time_th - 1/mu

    return rho, avg_packets_in_system_th, avg_waiting_time_th, avg_response_time_th, avg_queue_length_th