from typing import List, Optional

from dataclasses import dataclass, field

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.util.clock import Clock


@dataclass
class TraceLogRow:
    timestamp: int
    zone: str
    name: NamespacedName
    msg: str
    state: Optional[str] = None


@dataclass
class TraceLog:
    zone: str
    name: NamespacedName
    clock: Clock
    data: List[TraceLogRow] = field(default_factory=list)

    def log(self, msg: str) -> None:
        row = TraceLogRow(
            timestamp=self.clock.now_millis(),
            zone=self.zone,
            name=self.name,
            msg=msg,
        )
        self.data.append(row)

    def log_state(self, msg: str, state: str) -> None:
        row = TraceLogRow(
            timestamp=self.clock.now_millis(),
            zone=self.zone,
            name=self.name,
            msg=msg,
            state=state,
        )
        self.data.append(row)

    def get_raw(self) -> List[TraceLogRow]:
        return self.data

    def reset(self) -> None:
        self.data = []
