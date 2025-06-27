from dataclasses import dataclass


@dataclass
class DriverScore:
    driverId: int
    time: int

    def __hash__(self):
        return hash((self.driverId, self.time))

    def __eq__(self, other):
        return (self.driverId == other.driverId
                and self.time == other.time)