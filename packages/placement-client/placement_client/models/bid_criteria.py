from enum import Enum


class BidCriteria(str, Enum):
    CPU = "cpu"
    EPHEMERAL_STORAGE = "ephemeral-storage"
    MEMORY = "memory"
    NVIDIA_COMGPU = "nvidia.com/gpu"
    STORAGE = "storage"

    def __str__(self) -> str:
        return str(self.value)
