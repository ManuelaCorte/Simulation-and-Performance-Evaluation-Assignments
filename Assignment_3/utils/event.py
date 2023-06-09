from enum import Enum
import numpy as np
from queue import PriorityQueue


class Event:
    def __init__(self, type, time, idx = None, server = -1):
        self.type = type
        self.time = time
        self.idx = idx
        if (type == EventType.departure and server < 0):
            raise "Error: departure set without a specified server"
        self.server = server

    def __str__(self) -> str:
        if self.type == EventType.arrival or self.type == EventType.departure:
            return f"Event: {self.type} of packet {self.idx} on server {self.server} at {self.time}"
        return f"Event: {self.type} on server {self.server} at {self.time}"


EventType = Enum("Type", "start arrival departure stop debug")


class EventQueue:
    def __init__(self, simulation_time):
        self.queue = PriorityQueue()
        self.queue.put((0.0, Event(EventType.start, 0)))
        self.queue.put((simulation_time, Event(EventType.stop, simulation_time)))

    def __str__(self) -> str:
        string = ""
        for event in self.queue.queue:
            string += " " + event.__str__()
        return string
