from enum import StrEnum


class SchedulingState(StrEnum):
    NEW = "new"
    FETCH_APPLICATION_SPEC = "fetch_spec"
    BID_COLLECTION = "bid_collection"
    AWAITING_RETRY = "awaiting_retry"
    ASSIGNED = "assigned"


class ZoneBidState:
    NEW = "new"
