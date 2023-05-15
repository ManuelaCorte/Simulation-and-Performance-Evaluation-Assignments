import logging
import numpy as np
from utils.event import Event, EventType, EventQueue
from queue import Queue
import pandas as pd


def simulation_loop(simulation_time, l, mu, gen):
    logging.basicConfig(
        level=logging.INFO,
        filename="simulation.log",
        filemode="a",
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    # We don't want to fill up the queue, but have at most a couple of arrivals and a departure
    queue = EventQueue(simulation_time)

    current_event: Event = queue.queue.get()[1]
    current_time = current_event.time
    server_busy = False
    server_queue = Queue()
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
                server_busy = False

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
                if not server_busy:
                    # Seize server to serve packet and schedule its departure based on the exponentail service time
                    server_busy = True
                    service_time = gen.exponential(1 / mu)
                    # Note that the departure event added has the same idx as the arrival event that generated it
                    queue.queue.put(
                        (
                            current_event.time + service_time,
                            Event(
                                EventType.departure,
                                current_event.time + service_time,
                                current_event.idx,
                            ),
                        )
                    )
                    # A packet is being served so there are server_queue_size + 1 packets in the all system
                    queue_occupation.loc[current_time] = [
                        current_event.time,
                        server_queue.qsize(),
                        server_queue.qsize() + 1,
                        None,
                    ]

                    packets.loc[current_event.idx]["service_time"] = current_time
                    packets.loc[current_event.idx]["departure_time"] = (
                        current_time + service_time
                    )

                    logging.info(f"Server free, serving packet {current_event.idx}")
                else:
                    # Server busy, add arrived packet to server queue
                    server_queue.put(current_event)
                    queue_occupation.loc[current_time] = [
                        current_event.time,
                        server_queue.qsize(),
                        server_queue.qsize() + 1,
                        None,
                    ]
                    logging.info(
                        f"Server busy, packet {current_event.idx} added to queue at time {current_event.time}"
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

                if server_queue.empty():
                    # No package in the queue, free server
                    server_busy = False
                    queue_occupation.loc[current_time] = [
                        current_event.time,
                        0,
                        0,
                        None,
                    ]

                else:
                    # Since there was a departure the server is free to serve another packet --> pick one from the server queue
                    server_busy = True
                    pending_packet = server_queue.get()
                    service_time = gen.exponential(1 / mu)
                    queue.queue.put(
                        (
                            current_time + service_time,
                            Event(
                                EventType.departure,
                                current_event.time + service_time,
                                pending_packet.idx,
                            ),
                        )
                    )

                    queue_occupation.loc[current_time] = [
                        current_event.time,
                        server_queue.qsize(),
                        server_queue.qsize() + 1,
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
    packets['server_time'] = packets['departure_time'] - packets['service_time']
    packets["waiting_time"] = packets["service_time"] - packets["arrival_time"]
    packets["total_time"] = packets["departure_time"] - packets["arrival_time"]

    # Compute width of intervals in queue occupation
    queue_occupation["width"] = queue_occupation["time"].shift(-1) - queue_occupation["time"]
    # print(queue_occupation.head())

    # Drop rows with missing values (e.g. packets that entered the system but weren't served) (not sure if statistically correct)
    packets.dropna(inplace=True)
    queue_occupation.dropna(inplace=True)

    # Save dataframes to csv for easier inspection
    packets.to_csv("packets.csv")
    queue_occupation.to_csv("queue_occupation.csv")
    return packets, queue_occupation
