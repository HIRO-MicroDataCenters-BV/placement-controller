from typing import Dict, List, Mapping, Optional, Type

import copy
from dataclasses import dataclass, field

from application_client import models
from loguru import logger

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.scheduling_state import FSMOperation, SchedulingState
from placement_controller.core.types import SchedulingStep
from placement_controller.jobs.bid_action import BidResponseOrError
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

    current_zone: str
    available_zones: List[PlacementZone]
    application: AnyApplication

    retry_attempt: int = field(default=0)
    trace: TraceLog = field(default_factory=TraceLog)
    msg: Optional[str] = field(default=None)
    inprogress_actions: Dict[ActionId, Action[ActionResult]] = field(default_factory=dict)

    # lifecycle action arguments
    application_spec: Optional[models.ApplicationSpec] = field(default=None)
    bid_responses: Optional[Mapping[str, BidResponseOrError]] = field(default=None)
    decision: Optional[List[PlacementZone]] = field(default=None)

    # history tracking
    previous: Optional["SchedulingContext"] = field(default=None)

    @staticmethod
    def new(
        application: AnyApplication,
        timestamp: int,
        name: NamespacedName,
        current_zone: str,
        available_zones: List[PlacementZone],
    ) -> "SchedulingContext":
        return SchedulingContext(
            name=name,
            seq_nr=0,
            action_nr=0,
            timestamp=timestamp,
            state=SchedulingState.initial(timestamp),
            current_zone=current_zone,
            available_zones=available_zones,
            application=application,
        )

    def start_operation(self, operation: FSMOperation, timestamp: int) -> "SchedulingContext":
        msg = f"Starting {operation.direction}. desired replica: {operation.required_replica}"
        new_state = self.state.start_operation(timestamp, operation)
        return self.to_next_with_app(new_state, self.application, timestamp, msg)

    def to_next(self, step: SchedulingStep, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        new_state = self.state.to(step, timestamp)
        return self.to_next_with_app(new_state, self.application, timestamp, msg)

    def retry(self, timestamp: int, msg: Optional[str]) -> "SchedulingContext":
        retry_state = self.state.to(self.state.step, timestamp)
        context = self.to_next_with_app(retry_state, self.application, timestamp, msg)
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
            current_zone=self.current_zone,
            available_zones=copy.deepcopy(self.available_zones),
            retry_attempt=self.retry_attempt,
            msg=msg,
            inprogress_actions=copy.deepcopy(self.inprogress_actions),
            application=copy.deepcopy(application) if application else self.application,
            application_spec=copy.deepcopy(self.application_spec),
            bid_responses=copy.deepcopy(self.bid_responses),
            decision=copy.deepcopy(self.decision),
            previous=self,
            trace=self.trace,
        )

    def update_timestamp(self, expires_at: int) -> "SchedulingContext":
        self.state.expires_at = expires_at
        return self

    def update_application(self, application: AnyApplication) -> "SchedulingContext":
        self.application = application
        return self

    def with_action(self, action: Action[ActionResult]) -> "SchedulingContext":
        self.inprogress_actions[action.action_id] = action
        return self

    def with_available_zones(self, available_zones: List[PlacementZone]) -> "SchedulingContext":
        self.available_zones = available_zones
        return self

    def get_action_by_id(self, action_id: ActionId) -> Optional[Action[ActionResult]]:
        return self.inprogress_actions.get(action_id)

    def get_action_by_type(self, action_type: Type[Action[ActionResult]]) -> Optional[Action[ActionResult]]:
        for action in self.inprogress_actions.values():
            if isinstance(action, action_type):
                return action
        return None

    def with_application_spec(
        self, action_id: ActionId, application_spec: models.ApplicationSpec, timestamp: int, msg: str
    ) -> "SchedulingContext":
        context = self.to_next_with_app(self.state, self.application, timestamp, msg)
        context.application_spec = application_spec
        context.retry_attempt = 0
        del context.inprogress_actions[action_id]
        return context

    def with_bid_responses(
        self, action_id: ActionId, bid_responses: Mapping[str, BidResponseOrError], timestamp: int, msg: str
    ) -> "SchedulingContext":
        context = self.to_next_with_app(self.state, self.application, timestamp, msg)
        context.bid_responses = bid_responses
        context.retry_attempt = 0
        del context.inprogress_actions[action_id]
        return context

    def with_placement_decision(
        self, action_id: ActionId, decision: List[PlacementZone], timestamp: int, msg: str
    ) -> "SchedulingContext":
        context = self.to_next_with_app(self.state, self.application, timestamp, msg)
        context.decision = decision
        context.retry_attempt = 0
        del context.inprogress_actions[action_id]
        return context

    def with_placements_done(self, action_id: ActionId, timestamp: int, msg: str) -> "SchedulingContext":
        context = self.to_next_with_app(self.state, self.application, timestamp, msg)
        context.retry_attempt = 0
        del context.inprogress_actions[action_id]
        return context

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
