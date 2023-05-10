import logging
import numpy as np
from utils.event import Event, EventType, EventQueue
from utils.packet import Packet
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
    queue = EventQueue(
        simulation_time
    )  # don't fill up the queue, at most a couple of arrivals and a departure

    current_event: Event = queue.queue.get()[1]
    current_time = current_event.time
    packets_in_queue = 0
    server_busy = False
    server_queue = Queue()
    packets = pd.DataFrame(columns=["idx", "arrival_time", "service_time", "departure_time", "waiting_time", "response_time"])
    queue_occupation = pd.DataFrame(columns=['time', 'packets_in_queue', 'total_packets'])
    # queue.queue.put((2.60, Event(EventType.debug, 2.60, None)))
    # queue.queue.put((2.71, Event(EventType.debug, 2.71, None)))
    # logging.info(queue)
    while True:
        match current_event.type:
            case EventType.start:
                logging.info(f"Simulation started")

                # Schedule first arrival
                arr = gen.exponential(1 / l)
                queue.queue.put((arr, Event(EventType.arrival, arr, 0)))
                server_busy = False
                
                queue_occupation.loc['arr'+str(0)] = [0, 0, 0]
                packets.loc[0] = [0, arr, None, None, None, None]
                # logging.info(f'Scheduling first arrival at time {arr}')

            case EventType.stop:
                logging.info(f"Simulation completed")
                break

            case EventType.arrival:
                logging.info(
                    f"Packet {current_event.idx} arrived at time {current_event.time}"
                )
                packets.loc[current_event.idx] = [current_event.idx, current_event.time, None, None, None, None]
                if not server_busy:
                    # Schedule packet departure and seize server
                    server_busy = True
                    service_time = gen.exponential(1 / mu)
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
                    queue_occupation.loc['arr'+str(current_event.idx)] = [current_event.time, server_queue.qsize(), server_queue.qsize() +1]

                    logging.info(f"Server free, serving packet {current_event.idx}")
                    packets.loc[current_event.idx]['service_time'] = current_time
                    packets.loc[current_event.idx]['departure_time'] = current_time + service_time
                    # packets[current_event.idx].service_time = current_time
                    # packets[current_event.idx].departure_time = (
                    #     current_time + service_time
                    # )
                else:
                    # Server busy, add arrived packet to queue
                    server_queue.put(current_event)
                    queue_occupation.loc['arr'+str(current_event.idx)] = [current_event.time, server_queue.qsize(), server_queue.qsize() + 1]
                    logging.info(
                        f"Server busy, packet {current_event.idx} added to queue at time {current_event.time}"
                    )
                # logging.info(current_event)

                # Schedule next arrival so that the queue is never empty
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
                packets.loc[current_event.idx]['departure_time'] = current_time
                
                # packets[current_event.idx].departure_time = current_event.time
                if server_queue.empty():
                    queue_occupation.loc['dep'+str(current_event.idx)] = [current_event.time, 0, 0]

                    # No package in the queue, free server
                    server_busy = False
                    # logging.info('No packages in queue, server free')
                else:
                    # Serve new packet picking it from the queue
                    # queue.queue.put((current_event.time + gen.exponential(1/mu), Event(EventType.departure, current_event.time + gen.exponential(1/mu), current_event.idx )))
                    # logging.info(f'Picking package {current_event.idx} from queue and scheduling its departure')
                    pending_arrival = server_queue.get()
                    queue_occupation.loc['dep'+str(current_event.idx)] = [current_event.time, server_queue.qsize(), server_queue.qsize() + 1]
                    service_time = gen.exponential(1 / mu)
                    queue.queue.put(
                        (
                            current_time + service_time,
                            Event(
                                EventType.departure,
                                current_event.time + service_time,
                                pending_arrival.idx,
                            ),
                        )
                    )
                    logging.info(
                        f"Picking package {pending_arrival.idx} from queue and serving it at time {current_event.time}"
                    )
                    server_busy = True
                    packets.loc[pending_arrival.idx]['service_time'] = current_time
                    packets.loc[pending_arrival.idx]['departure_time'] = current_time + service_time
                    # packets.update(
                    #     {
                    #         pending_arrival.idx: Packet(
                    #             pending_arrival.idx,
                    #             pending_arrival.time,
                    #             current_time,
                    #             current_event.time + service_time,
                    #         )
                    #     }
                    # )
            case EventType.debug:
                breakpoint()
            case _:
                logging.info(
                    f"Unknown event type {current_event.type} {current_event.time}"
                )

        current_event = queue.queue.get()[1]
        current_time = current_event.time

    packets['waiting_time'] = packets['service_time'] - packets['arrival_time']
    packets['response_time'] = packets['departure_time'] - packets['arrival_time']
    # print(packets.head())
    # print(queue_occupation.head())
    packets.to_csv('packets.csv')
    queue_occupation.to_csv('queue_occupation.csv')
    return packets, queue_occupation