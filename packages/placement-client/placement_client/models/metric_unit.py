from enum import Enum


class MetricUnit(str, Enum):
    BYTE = "byte"
    CORE = "core"
    EUR = "eur"
    WATT = "watt"

    def __str__(self) -> str:
        return str(self.value)
