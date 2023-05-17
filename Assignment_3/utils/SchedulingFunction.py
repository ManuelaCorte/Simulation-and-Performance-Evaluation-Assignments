import numpy as np
from queue import Queue
import pandas as pd
from enum import Enum

SchedulingFunction = Enum('SchedulingFunction', ['RoundRobin', 'LeastFull', 'Random'])

def LeastFull(n_servers, servers_queue: list[Queue]):
    server_choosen = 0
    for i in range(n_servers):
        if servers_queue[i].qsize() < servers_queue[server_choosen].qsize():
            server_choosen = i
    return server_choosen

def RoundRobin(n_servers, servers_queue: list[Queue], max_queue_elements, round_robin_index):
    server_choosen = round_robin_index

    while True:
        if servers_queue[server_choosen].qsize() < max_queue_elements: break
        # server_choosen is full, try the next one
        server_choosen = (server_choosen + 1) % n_servers
        # we looped back to the first server: all of them are full, so just return the first. the packet will be discarded later
        if server_choosen == round_robin_index: break

    round_robin_index = (server_choosen + 1) % n_servers
    return server_choosen, round_robin_index

def Random(n_servers, servers_queue: list[Queue], max_queue_elements):
    servers_not_full = []
    for i in range(n_servers):
        if servers_queue[i].qsize() < max_queue_elements:
            servers_not_full.append(i)
    # all servers are full, so return whatever. the packet will be discarded later
    if len(servers_not_full) == 0:
        return 0

    server_choosen = servers_not_full[np.random.randint(len(servers_not_full))]
    return server_choosen