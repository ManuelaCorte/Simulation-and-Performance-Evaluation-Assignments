class Packet:
    def __init__(self, idx, arrival_time, service_time, departure_time) -> None:
        self.idx = idx
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.departure_time = departure_time

    def compute_waiting_time(self):
        return (
            self.service_time - self.arrival_time
            if self.service_time is not None
            else None
        )

    def compute_server_occupation_time(self):
        return (
            self.departure_time - self.service_time
            if self.departure_time is not None and self.service_time is not None
            else None
        )

    def compute_total_time(self):
        return (
            self.departure_time - self.arrival_time
            if self.departure_time is not None
            else None
        )

    def __str__(self) -> str:
        return f"Packet {self.idx} arrived at {self.arrival_time}, served at {self.service_time}, departed at {self.departure_time}"
