from enum import Enum


class BidCriteria(str, Enum):
    CPU = "cpu"
    EPHEMERAL_STORAGE = "ephemeral-storage"
    GPU = "gpu"
    PVC_STORAGE = "pvc-storage"
    RAM = "ram"

    def __str__(self) -> str:
        return str(self.value)
