from typing import Any, Dict

from dataclasses import dataclass
from enum import StrEnum


class EventType(StrEnum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"


@dataclass
class K8SEvent:
    event: EventType
    version: int
    object: Dict[str, Any]
