import logging
import numpy as np
from utils.event import Event, EventType, EventQueue
from queue import Queue
from utils.SchedulingFunction import SchedulingFunction, RoundRobin, LeastFull, Random
import pandas as pd
import time

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
    logging.disable(logging.INFO)

    # We don't want to fill up the queue, but have at most a couple of arrivals and a departure
    queue = EventQueue(simulation_time)

    current_event: Event = queue.queue.get()[1]
    current_time = current_event.time
    servers_busy = [False for i in range(n_servers)]
    servers_queue = [Queue() for i in range(n_servers)]
    # Dataframe to store time information about packets
    packets = pd.DataFrame(
        columns=[
            "idx",
            "arrival_time",
            "service_time",
            "departure_time",
            "waiting_time",
            "total_time",
        ]
    )
    # Dataframe to store the packets in queue and the system at every time jump (and the width of that jump)
    # The widths of all jumps are computed at the end as the difference between the current time and the previous one
    queue_occupation = pd.DataFrame(
        columns=["time", "packets_in_queue", "total_packets", "width"]
    )

    while True:
        match current_event.type:
            case EventType.start:
                logging.info(f"Simulation started")

                # Schedule first arrival
                arr = gen.exponential(1 / l)
                queue.queue.put((arr, Event(EventType.arrival, arr, 0)))

                packets.loc[0] = [0, arr, None, None, None, None]

                # Initial condition: system empty until first arrival
                queue_occupation.loc[0.0] = [0.0, 0, 0, arr]

            case EventType.stop:
                logging.info(f"Simulation completed")
                break

            case EventType.arrival:
                logging.info(
                    f"Packet {current_event.idx} arrived at time {current_event.time}"
                )
                packets.loc[current_event.idx] = [
                    current_event.idx,
                    current_event.time,
                    None,
                    None,
                    None,
                    None,
                ]

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
                        queue_occupation.loc[current_time] = [
                            current_event.time,
                            servers_queue[server_choosen].qsize(),
                            servers_queue[server_choosen].qsize() + 1,
                            None,
                        ]

                        packets.loc[current_event.idx]["service_time"] = current_time
                        packets.loc[current_event.idx]["departure_time"] = (
                            current_time + service_time
                        )

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
                        queue_occupation.loc[current_time] = [
                            current_event.time,
                            servers_queue[server_choosen].qsize(),
                            servers_queue[server_choosen].qsize() + 1,
                            None,
                        ]
                        logging.info(
                            f"All servers busy, packet {current_event.idx} added to queue {server_choosen} at time {current_event.time}"
                        )
                    else:
                        # TODO ADD LOGGING FOR DISCARDED PACKETS
                        queue_occupation.loc[current_time] = [
                            current_event.time,
                            servers_queue[server_choosen].qsize(),
                            servers_queue[server_choosen].qsize(),
                            None,
                        ]
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
                        ),
                    )
                )

            case EventType.departure:
                logging.info(
                    f"Packet {current_event.idx} departed at time {current_event.time}"
                )
                # Update the departure time of the packet
                packets.loc[current_event.idx]["departure_time"] = current_time
                server_choosen = current_event.server

                if servers_queue[server_choosen].empty():
                    # No package in the queue, free server
                    servers_busy[server_choosen] = False
                    queue_occupation.loc[current_time] = [
                        current_event.time,
                        0,
                        0,
                        None,
                    ]

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

                    queue_occupation.loc[current_time] = [
                        current_event.time,
                        servers_queue[server_choosen].qsize(),
                        servers_queue[server_choosen].qsize() + 1,
                        None,
                    ]
                    packets.loc[pending_packet.idx]["service_time"] = current_time
                    packets.loc[pending_packet.idx]["departure_time"] = (
                        current_time + service_time
                    )
                    logging.info(
                        f"Picking package {pending_packet.idx} from queue and serving it at time {current_event.time}"
                    )
            case EventType.debug:
                # If we see any weird behaviour at time t we can add two breakpoint events one slightly before and one slightly after t
                breakpoint()
            case _:
                logging.info(
                    f"Unknown event type {current_event.type} {current_event.time}"
                )
                break

        current_event = queue.queue.get()[1]
        current_time = current_event.time

    # Compute waiting and total time for each packet
    packets["server_time"] = packets["departure_time"] - packets["service_time"]
    packets["waiting_time"] = packets["service_time"] - packets["arrival_time"]
    packets["total_time"] = packets["departure_time"] - packets["arrival_time"]

    # Compute width of intervals in queue occupation
    queue_occupation["width"] = (
        queue_occupation["time"].shift(-1) - queue_occupation["time"]
    )
    # print(queue_occupation.head())

    # Drop rows with missing values (e.g. packets that entered the system but weren't served) (not sure if statistically correct)
    packets.dropna(inplace=True)
    queue_occupation.dropna(inplace=True)
    print("--- %s seconds ---" % (time.time() - start_time))

    # Save dataframes to csv for easier inspection
    packets.to_csv("packets.csv")
    queue_occupation.to_csv("queue_occupation.csv")
    return packets, queue_occupation
