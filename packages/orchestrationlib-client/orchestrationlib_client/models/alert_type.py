from enum import Enum


class AlertType(str, Enum):
    ABNORMAL = "Abnormal"
    NETWORK_ATTACK = "Network-Attack"
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)
