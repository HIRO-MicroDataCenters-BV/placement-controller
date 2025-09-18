from enum import Enum


class BidStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
