from typing import Optional

from dataclasses import dataclass, field

from application_client import models

from placement_controller.core.application import AnyApplication
from placement_controller.core.types import SchedulingState


@dataclass
class SchedulingContext:
    seq_nr: int
    timestamp: int
    state: SchedulingState
    msg: Optional[str] = field(default=None)
    application: Optional[AnyApplication] = field(default=None)
    application_spec: Optional[models.ApplicationSpec] = field(default=None)

    @staticmethod
    def new(timestamp: int) -> "SchedulingContext":
        return SchedulingContext(seq_nr=0, timestamp=timestamp, state=SchedulingState.NEW)

    def to_next(self, state: SchedulingState, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        return self.to_next_with_app(state, self.application, timestamp, msg)

    def to_next_with_app(
        self, state: SchedulingState, application: Optional[AnyApplication], timestamp: int, msg: Optional[str]
    ) -> "SchedulingContext":
        return SchedulingContext(
            seq_nr=self.seq_nr + 1, timestamp=timestamp, state=state, msg=msg, application=application
        )
