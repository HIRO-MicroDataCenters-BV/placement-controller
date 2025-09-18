from enum import Enum


class Metric(str, Enum):
    COST = "cost"
    ENERGY = "energy"

    def __str__(self) -> str:
        return str(self.value)
