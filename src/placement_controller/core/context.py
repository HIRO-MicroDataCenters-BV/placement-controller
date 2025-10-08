from typing import Dict, Optional, Type

from dataclasses import dataclass, field

from application_client import models

from placement_controller.core.application import AnyApplication
from placement_controller.core.types import SchedulingState
from placement_controller.jobs.types import Action, ActionId, ActionResult


@dataclass
class SchedulingContext:
    seq_nr: int
    timestamp: int
    state: SchedulingState
    retry_attempt: int = field(default=0)
    msg: Optional[str] = field(default=None)
    inprogress_actions: Dict[ActionId, Action[ActionResult]] = field(default_factory=dict)
    application: Optional[AnyApplication] = field(default=None)
    application_spec: Optional[models.ApplicationSpec] = field(default=None)

    @staticmethod
    def new(timestamp: int) -> "SchedulingContext":
        return SchedulingContext(seq_nr=0, timestamp=timestamp, state=SchedulingState.NEW)

    def to_next(self, state: SchedulingState, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        return self.to_next_with_app(state, self.application, timestamp, msg)

    def retry(self, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        # TODO attempts
        return self.to_next_with_app(self.state, self.application, timestamp, msg)

    def to_next_with_app(
        self, state: SchedulingState, application: Optional[AnyApplication], timestamp: int, msg: Optional[str]
    ) -> "SchedulingContext":
        return SchedulingContext(
            seq_nr=self.seq_nr + 1, timestamp=timestamp, state=state, msg=msg, application=application
        )

    def get_action_by_id(self, action_id: ActionId) -> Optional[Action[ActionResult]]:
        return self.inprogress_actions.get(action_id)

    def get_action_by_type(self, action_type: Type[Action[ActionResult]]) -> Optional[Action[ActionResult]]:
        for action in self.inprogress_actions.values():
            if isinstance(action, action_type):
                return action
        return None

    def is_attempts_exhausted(self) -> bool:
        return False

    def inprogress_actions_count(self) -> int:
        return len(self.inprogress_actions)
