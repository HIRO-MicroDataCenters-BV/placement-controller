from enum import StrEnum


class SchedulingState(StrEnum):
    NEW = "new"
    AWAITING_RETRY = "awaiting_retry"
    ASSIGNED = "assigned"
