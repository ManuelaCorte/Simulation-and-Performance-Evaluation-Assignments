import logging
import numpy as np
from utils.event import Event, EventType, EventQueue
from queue import Queue
from utils.SchedulingFunction import SchedulingFunction, RoundRobin, LeastFull, Random
import pandas as pd
import time
import os
def simulation_loop(
        simulation_time, 
        l, 
        mu, 
        gen, 
        n_servers = 1, 
        max_queue_elements = np.inf, 
        scheduling_function = SchedulingFunction.LeastFull
    ):

    start_time = time.time()
    if scheduling_function == SchedulingFunction.RoundRobin:
        round_robin_index = 0
    logging.basicConfig(
        level=logging.INFO,
        filename="simulation.log",
        filemode="a",
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    # If not needed, logging turned off to speed up simulation
    # logging.disable(logging.INFO)

    # We don't want to fill up the queue, but have at most a couple of arrivals and a departure
    queue = EventQueue(simulation_time)

    current_event: Event = queue.queue.get()[1]
    current_time = current_event.time
    servers_busy = [False for i in range(n_servers)]
    servers_queue = [Queue() for i in range(n_servers)]

    # Lists of dictionaries to store statistics
    packets = []
    queue_occupation = []
    discarded_packets = []
    
    i = 0

    while True:
        match current_event.type:
            case EventType.start:
                logging.info(f"Simulation started")
                # Remove csv files if they exist
                try:
                    os.remove("packets.csv")
                    os.remove("queue_occupation.csv")
                    os.remove("discarded_packets.csv")
                except OSError:
                    pass

                # Schedule first arrival in first server
                arr = gen.exponential(1 / l)
                queue.queue.put((arr, Event(EventType.arrival, arr, 0)))

                # packets.append({'idx':0, 'server_idx':0, 'arrival_time':arr, 'service_time':None, 'departure_time': None, 'waiting_time':None, 'total_time':None})

                # Initial condition: system empty until first arrival
                queue_occupation.append({'time':0.0, 'server_idx':None, 'packets_in_queue':0, 'total_packets':0, 'width':arr})

            case EventType.stop:
                logging.info(f"Simulation completed")
                break

            case EventType.arrival:
                logging.info(
                    f"Packet {current_event.idx} arrived at time {current_event.time}"
                )
                packet = {'idx': current_event.idx, 'server_idx': None, 'arrival_time': current_event.time, 'service_time': None, 'departure_time': None, 'waiting_time': None, 'total_time': None}
                packets.append(packet)

                # Find a server that is not busy and serve the package
                server_choosen = 0
                found_free_server = False
                while server_choosen < n_servers:
                    if servers_busy[server_choosen]:
                        server_choosen = server_choosen + 1
                    else:
                        found_free_server = True
                        # Seize server to serve packet and schedule its departure based on the exponentail service time
                        servers_busy[server_choosen] = True
                        service_time = gen.exponential(1 / mu)
                        # Note that the departure event added has the same idx as the arrival event that generated it
                        queue.queue.put(
                            (
                                current_event.time + service_time,
                                Event(
                                    EventType.departure,
                                    current_event.time + service_time,
                                    current_event.idx,
                                    server_choosen,
                                ),
                            )
                        )
                        # A packet is being served so there are server_queue_size + 1 packets in the all system
                        event = {'time':current_time, 'server_idx':server_choosen, 'packets_in_queue':servers_queue[server_choosen].qsize() , 'total_packets':servers_queue[server_choosen].qsize() + 1, 'width':None}
                        queue_occupation.append(event)

                        packets[current_event.idx]['server_idx'] = server_choosen
                        packets[current_event.idx]['service_time'] = current_time 
                        packets[current_event.idx]['departure_time'] = current_time + service_time

                        logging.info(f"Server {server_choosen} free, serving packet {current_event.idx}")

                
                if not found_free_server:
                    match scheduling_function:
                        case SchedulingFunction.LeastFull:
                            server_choosen = LeastFull(n_servers, servers_queue)
                        case SchedulingFunction.RoundRobin:
                            server_choosen, round_robin_index = RoundRobin(n_servers, servers_queue, max_queue_elements, round_robin_index)
                        case SchedulingFunction.Random:
                            server_choosen = Random(n_servers, servers_queue, max_queue_elements)
                        case _:
                            server_choosen = 0
                        
                    if servers_queue[server_choosen].qsize() <= max_queue_elements:
                        servers_queue[server_choosen].put(current_event)
                        # print(current_event)
                        event = {'time':current_time, 'server_idx':server_choosen, 'packets_in_queue':servers_queue[server_choosen].qsize() , 'total_packets':servers_queue[server_choosen].qsize() + 1, 'width':None}
                        queue_occupation.append(event)

                        logging.info(
                            f"All servers busy, packet {current_event.idx} added to queue {server_choosen} at time {current_event.time}"
                        )
                    else:
                        # Discarded packets are assigned server None
                        packets[current_event.idx]['server_idx'] = None   
                        discarded_packets.append({'idx': current_event.idx, 'arrival_time': current_event.time, 'server_idx': None})     
                        event = {'time':current_time, 'server_idx':None, 'packets_in_queue':servers_queue[server_choosen].qsize() , 'total_packets':servers_queue[server_choosen].qsize(), 'width':None}
                        queue_occupation.append(event)                      

                        logging.info(
                            f"Queue {server_choosen} full, packet {current_event.idx} discarded at time {current_event.time}"
                        )

                # Regardless of whether the server is busy or not schedule next arrival so that the queue is never empty
                interarrival_time = gen.exponential(1 / l)
                queue.queue.put(
                    (
                        current_event.time + interarrival_time,
                        Event(
                            EventType.arrival,
                            current_event.time + interarrival_time,
                            current_event.idx + 1,
                            None
                        ),
                    )
                )

            case EventType.departure:
                logging.info(
                    f"Packet {current_event.idx} departed at time {current_event.time}"
                )
                # Update the departure time of the packet
                packets[current_event.idx]["departure_time"] = current_time
                server_choosen = current_event.server

                if servers_queue[server_choosen].empty():
                    # No package in the queue, free server
                    servers_busy[server_choosen] = False
                    event = {'time':current_time, 'server_idx':server_choosen, 'packets_in_queue':0 , 'total_packets':0, 'width':None}
                    queue_occupation.append(event) 

                else:
                    # Since there was a departure the server is free to serve another packet --> pick one from the server queue
                    servers_busy[server_choosen] = True
                    pending_packet = servers_queue[server_choosen].get()
                    service_time = gen.exponential(1 / mu)
                    queue.queue.put(
                        (
                            current_time + service_time,
                            Event(
                                EventType.departure,
                                current_event.time + service_time,
                                pending_packet.idx,
                                server_choosen
                            ),
                        )
                    )

                    event = {'time':current_time, 'server_idx':server_choosen, 'packets_in_queue':servers_queue[server_choosen].qsize() , 'total_packets':servers_queue[server_choosen].qsize() + 1, 'width':None}
                    queue_occupation.append(event)          

                    packets[pending_packet.idx]["server_idx"] = server_choosen
                    packets[pending_packet.idx]["service_time"] = current_time
                    packets[pending_packet.idx]["departure_time"] = (
                        current_time + service_time
                    )
                    logging.info(
                        f"Picking package {pending_packet.idx} from queue and serving it at time {current_time}"
                    )
            case EventType.debug:
                # If we see any weird behaviour at time t we can add two breakpoint events one slightly before and one slightly after t
                breakpoint()
            case _:
                logging.info(
                    f"Unknown event type {current_event.type} {current_event.time}"
                )
                break 
  
        # if i % 5000 == 0 and i != 0:
        #     print(f'time: {current_time}')
        # i += 1
        current_event = queue.queue.get()[1]
        current_time = current_event.time   
        

    packets_save = pd.DataFrame(packets)
    queue_occupation_save = pd.DataFrame(queue_occupation)
    discarded_packets_save = pd.DataFrame(discarded_packets)
    
    # Compute waiting and total time for each packet
    packets_save["waiting_time"] = packets_save["service_time"] - packets_save["arrival_time"]
    packets_save["server_time"] = packets_save["departure_time"] - packets_save["service_time"]
    packets_save["total_time"] = packets_save["departure_time"] - packets_save["arrival_time"]

    # Compute width of intervals in queue occupation
    queue_occupation_save["width"] = (
        queue_occupation_save["time"].shift(-1) - queue_occupation_save["time"]
    )
    # print(queue_occupation_save.head())

    # Drop rows with missing values (e.g. packets that entered the system but weren't served) (not sure if statistically correct)
    packets_save.dropna(inplace=True)
    queue_occupation_save.dropna(inplace=True)
    discarded_packets_save.dropna(inplace=True)
    print("--- %s seconds ---" % (time.time() - start_time))

    queue_occupation_save['server_idx'] = queue_occupation_save['server_idx'].astype(int)
    
    # Save dataframes to csv for easier inspection
    packets_save.to_csv("packets.csv", index=False)
    queue_occupation_save.to_csv("queue_occupation.csv", index=False)
    discarded_packets_save.to_csv("discarded_packets.csv", index=False)
    return packets_save, queue_occupation_save, discarded_packets_save
