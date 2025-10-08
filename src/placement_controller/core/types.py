from enum import StrEnum


class SchedulingState(StrEnum):
    NEW = "new"
    FETCH_APPLICATION_SPEC = "fetch_spec"
    BID_COLLECTION = "bid_collection"
    DECISION = "decision"
    DONE = "done"
