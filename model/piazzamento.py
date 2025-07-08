from dataclasses import dataclass


@dataclass
class Piazzamento:
    raceId: int
    driverId: int
    time: str


    def __eq__(self, other):
        return self.raceId == other.raceId and self.driverId == other.driverId

    def __hash__(self):
        return hash((self.raceId, self.driverId))

    def __str__(self):
        return f"{self.raceId}-{self.driverId}-{self.time}"