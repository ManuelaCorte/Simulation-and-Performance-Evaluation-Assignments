def calculate_P0(rho, K):
    if K < float('inf'):
        numerator = 1 - rho
        denominator = 1 - (rho ** (K + 1))
        P0 = numerator / denominator
    else:
        P0 = 1 - rho
    
    return P0


def calculate_Ls(rho, l, mu, c, K):
    P0 = calculate_P0(rho, K)
    if K < float('inf'):
        Ls = P0 * (l / (mu * (1 - (l / (mu * c))))) + (K * l) / (mu * c)
    else:
        Ls = l / (mu * (1 - (l / (mu * c))))
    
    return Ls

def calculate_Wq(Lq, l, rho, K):
    if K < float('inf'):
        numerator = Lq
        denominator = l * (1 - calculate_P0(rho, K))
        Wq = numerator / denominator
    else:
        Wq = Lq / l
    return Wq


def calculate_Lq(Ls, l, mu):
    Lq = Ls - (l / mu)
    return Lq


def calculate_Ts(mu):
    Ts = 1 / mu
    return Ts


def calculate_Ws(Ls, l):
    Ws = Ls / l
    return Ws


def calculate_W(Ws, Ts):
    W = Ws - Ts
    return W


def compute_theoretical_statistics(l, mu, n_servers = 2, max_queue_elements = 1000):
    c = n_servers
    K = max_queue_elements

    # Calculate rho and check if it's less than 1
    rho = l / (mu * c)
    if rho >= 1:
        raise ValueError("The system is not underutilized (rho >= 1).")
    
    # Calculate the results
    Ls = calculate_Ls(rho, l, mu, c, K)
    Lq = calculate_Lq(Ls, l, mu)
    Wq = calculate_Wq(Lq, rho, c, K)
    Ts = calculate_Ts(mu)
    Ws = calculate_Ws(Ls, l)
    W = calculate_W(Ws, Ts)

    print("Average number of packets in the system (Ls):", Ls)
    print("Average queue length (Lq):", Lq)
    print("Average waiting time (Wq):", Wq)
    print("Average service time (Ts):", Ts)
    print("Average time in the system (Ws):", Ws)
    print("Average time in the system (W):", W)

    avg_packets_in_system_th = Ls
    avg_waiting_time_th = W
    avg_response_time_th = Wq
    avg_queue_length_th = Lq
    return rho, avg_packets_in_system_th, avg_waiting_time_th, avg_response_time_th, avg_queue_length_th

if __name__ == '__main__':
    # Example usage
    
    # Define the input parameters
    l = 0.5  # Arrival rate
    mu = 1.0  # Service rate
    c = 2  # Number of servers
    K = 5  # System capacity
    
    # Calculate rho and check if it's less than 1
    rho = l / (mu * c)
    if rho >= 1:
        raise ValueError("The system is not underutilized (rho >= 1).")
    
    # Calculate the results
    P0 = calculate_P0(rho, K)
    Ls = calculate_Ls(rho, l, mu, c, K)
    Lq = calculate_Lq(Ls, l, mu)
    Wq = calculate_Wq(Lq, rho, c, K)
    Ts = calculate_Ts(mu)
    Ws = calculate_Ws(Ls, l)
    W = calculate_W(Ws, Ts)
    
    # Print the results
    print("Stationary probability of zero customers (P0):", P0)
    print("Average number of packets in the system (Ls):", Ls)
    print("Average queue length (Lq):", Lq)
    print("Average waiting time (Wq):", Wq)
    print("Average service time (Ts):", Ts)
    print("Average time in the system (Ws):", Ws)
    print("Average time in the system (W):", W)
