from typing import Dict, List, Set

from dataclasses import dataclass

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM
from placement_controller.core.types import SchedulingState
from placement_controller.jobs.types import Action, ActionResult
from placement_controller.membership.types import Membership, PlacementZone
from placement_controller.util.clock import Clock


@dataclass
class ApplicationState:
    seq_nr: int
    state: SchedulingState
    running_jobs: List[str]
    history: List["ApplicationState"]


class SchedulingQueue:
    clock: Clock
    contexts: Dict[NamespacedName, SchedulingContext]
    zones: Set[PlacementZone]

    def __init__(self, clock: Clock):
        self.contexts = dict()
        self.zones = set()
        self.clock = clock

    def on_tick(self, timestamp: int) -> List[Action[ActionResult]]:
        actions = []
        for name in self.contexts.keys():
            context = self.contexts[name]
            next_state = FSM(context, timestamp).on_tick()
            if next_state.context:
                self.contexts[name] = next_state.context
            if next_state.actions:
                actions.extend(next_state.actions)
        return actions

    def on_membership_update(self, membership: Membership, timestamp: int) -> List[Action[ActionResult]]:
        self.zones = membership.zones

        actions = []
        for name in self.contexts.keys():
            context = self.contexts[name]
            next_state = FSM(context, timestamp).on_membership_change(self.zones)
            if next_state.context:
                self.contexts[name] = next_state.context
            if next_state.actions:
                actions.extend(next_state.actions)

        return actions

    def on_application_update(self, application: AnyApplication, timestamp: int) -> List[Action[ActionResult]]:
        context = self.get_context(application.get_namespaced_name(), timestamp)
        next_state = FSM(context, timestamp).next_state(application)
        if next_state.context:
            self.contexts[application.get_namespaced_name()] = next_state.context
        return next_state.actions

    def on_application_delete(self, application: AnyApplication, timestamp: int) -> List[Action[ActionResult]]:
        name = application.get_namespaced_name()
        del self.contexts[name]
        return []

    def on_action_result(self, result: ActionResult, timestamp: int) -> List[Action[ActionResult]]:
        context = self.get_context(result.get_application_name(), timestamp)
        next_state = FSM(context, timestamp).on_action_result(result)
        if next_state.context:
            self.contexts[result.get_application_name()] = next_state.context
        return next_state.actions

    def get_context(self, name: NamespacedName, timestamp: int) -> SchedulingContext:
        if name not in self.contexts:
            self.contexts[name] = SchedulingContext.new(timestamp)

        return self.contexts[name]

    def get_scheduling_states(self) -> List[ApplicationState]:
        return []
