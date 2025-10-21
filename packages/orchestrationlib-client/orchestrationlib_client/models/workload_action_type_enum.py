from enum import Enum


class WorkloadActionTypeEnum(str, Enum):
    BIND = "bind"
    CREATE = "create"
    DELETE = "delete"
    MOVE = "move"
    SWAP_X = "swap_x"
    SWAP_Y = "swap_y"

    def __str__(self) -> str:
        return str(self.value)
