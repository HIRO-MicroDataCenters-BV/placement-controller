from enum import Enum


class WorkloadRequestDecisionStatusEnum(str, Enum):
    FAILED = "failed"
    PENDING = "pending"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
