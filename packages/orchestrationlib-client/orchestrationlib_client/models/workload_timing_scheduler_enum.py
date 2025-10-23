from enum import Enum


class WorkloadTimingSchedulerEnum(str, Enum):
    DEFAULT_SCHEDULER = "default-scheduler"
    RESOURCE_MANAGEMENT_SERVICE = "resource-management-service"

    def __str__(self) -> str:
        return str(self.value)
