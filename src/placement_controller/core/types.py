from enum import StrEnum


class SchedulingStep(StrEnum):
    PENDING = "pending"
    FETCH_APPLICATION_SPEC = "fetch_spec"
    BID_COLLECTION = "bid_collection"
    DECISION = "decision"
    SET_PLACEMENT = "set_placement"
    DONE = "done"
