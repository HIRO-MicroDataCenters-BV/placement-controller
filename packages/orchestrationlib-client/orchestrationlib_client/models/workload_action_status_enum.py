from enum import Enum


class WorkloadActionStatusEnum(str, Enum):
    FAILED = "failed"
    PENDING = "pending"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
