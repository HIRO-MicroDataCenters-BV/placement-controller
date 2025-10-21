from typing import Any, Dict, List, Union

from dataclasses import dataclass
from enum import StrEnum


class EventType(StrEnum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"
    SNAPSHOT = "SNAPSHOT"


KubeObject = Dict[str, Any]


@dataclass
class KubeEvent:
    event: EventType
    version: int
    object: Union[KubeObject, List[KubeObject]]
