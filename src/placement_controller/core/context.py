from typing import Dict, List, Optional, Type

from dataclasses import dataclass, field

from application_client import models
from loguru import logger

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.types import SchedulingState
from placement_controller.jobs.types import Action, ActionId, ActionResult
from placement_controller.membership.types import PlacementZone
from placement_controller.resources.trace_log import TraceLog

DEFAULT_ACTION_TIMEOUT_SECONDS: int = 60
DEFAULT_MAX_ACTION_ATTEMPTS: int = 3


@dataclass
class SchedulingContext:
    name: NamespacedName
    seq_nr: int
    action_nr: int
    timestamp: int
    state: SchedulingState
    placement_zones: List[PlacementZone]
    retry_attempt: int = field(default=0)
    trace: TraceLog = field(default_factory=TraceLog)
    msg: Optional[str] = field(default=None)
    inprogress_actions: Dict[ActionId, Action[ActionResult]] = field(default_factory=dict)
    application: Optional[AnyApplication] = field(default=None)
    application_spec: Optional[models.ApplicationSpec] = field(default=None)
    previous: Optional["SchedulingContext"] = field(default=None)

    @staticmethod
    def new(timestamp: int, name: NamespacedName, placement_zones: List[PlacementZone]) -> "SchedulingContext":
        return SchedulingContext(
            name=name,
            seq_nr=0,
            action_nr=0,
            timestamp=timestamp,
            state=SchedulingState.NEW,
            placement_zones=placement_zones,
        )

    def to_next(self, state: SchedulingState, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        return self.to_next_with_app(state, self.application, timestamp, msg)

    def retry(self, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        context = self.to_next_with_app(self.state, self.application, timestamp, msg)
        context.retry_attempt += 1
        return context

    def to_next_with_app(
        self, state: SchedulingState, application: Optional[AnyApplication], timestamp: int, msg: Optional[str]
    ) -> "SchedulingContext":
        logger.info(f"{self.name.to_string()}: state={state}, msg='{msg}', ts={timestamp}")
        self.trace.log(f"{self.name.to_string()}: state={state}, msg='{msg}', ts={timestamp}")
        return SchedulingContext(
            name=self.name,
            seq_nr=self.seq_nr + 1,
            action_nr=self.action_nr,
            timestamp=timestamp,
            state=state,
            placement_zones=self.placement_zones,
            retry_attempt=self.retry_attempt,
            msg=msg,
            inprogress_actions=self.inprogress_actions,
            application=application,
            application_spec=self.application_spec,
            previous=self,
            trace=self.trace,
        )

    def with_action(self, action: Action[ActionResult]) -> "SchedulingContext":
        self.inprogress_actions[action.action_id] = action
        return self

    def with_placement_zones(self, placement_zones: List[PlacementZone]) -> "SchedulingContext":
        self.placement_zones = placement_zones
        return self

    def get_action_by_id(self, action_id: ActionId) -> Optional[Action[ActionResult]]:
        return self.inprogress_actions.get(action_id)

    def get_action_by_type(self, action_type: Type[Action[ActionResult]]) -> Optional[Action[ActionResult]]:
        for action in self.inprogress_actions.values():
            if isinstance(action, action_type):
                return action
        return None

    def is_attempts_exhausted(self) -> bool:
        return self.retry_attempt >= DEFAULT_MAX_ACTION_ATTEMPTS

    def is_timeout(self, now: int) -> bool:
        return (now - self.timestamp) > DEFAULT_ACTION_TIMEOUT_SECONDS * 1000

    def inprogress_actions_count(self) -> int:
        return len(self.inprogress_actions)

    def gen_action_id(self) -> str:
        action_nr = self.action_nr
        self.action_nr += 1
        return f"{action_nr}"
