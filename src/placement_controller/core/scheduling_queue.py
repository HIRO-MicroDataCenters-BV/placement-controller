from typing import Dict, List, Optional, Set

from placement_controller.api.model import ApplicationState, SchedulingEntry
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM, FSMOptions
from placement_controller.core.next_state_result import NextStateResult
from placement_controller.core.scheduling_state import DEFAULT_FAILURE_DELAY_SECONDS, DEFAULT_RESCHEDULE_DELAY_SECONDS
from placement_controller.jobs.types import Action, ActionResult
from placement_controller.membership.types import Membership, PlacementZone
from placement_controller.util.clock import Clock


class SchedulingQueue:
    clock: Clock
    contexts: Dict[NamespacedName, SchedulingContext]
    zones: Set[PlacementZone]
    current_zone: str

    def __init__(self, clock: Clock, current_zone: str):
        self.contexts = dict()
        self.zones = set()
        self.clock = clock
        self.current_zone = current_zone

    def on_tick(self, timestamp: int) -> List[Action[ActionResult]]:
        actions = []
        for name in self.contexts.keys():
            context = self.contexts[name]
            next_state = self.new_fsm(context, timestamp).on_tick()

            self.apply_next_state(name, next_state)

            if next_state.actions:
                actions.extend(next_state.actions)

        return actions

    def on_membership_update(self, membership: Membership, timestamp: int) -> List[Action[ActionResult]]:
        self.zones = membership.zones

        actions = []
        for name in self.contexts.keys():
            context = self.contexts[name]
            next_state = self.new_fsm(context, timestamp).on_membership_change(list(self.zones))
            self.apply_next_state(name, next_state)

            if next_state.actions:
                actions.extend(next_state.actions)

        return actions

    def on_application_update(self, application: AnyApplication, timestamp: int) -> List[Action[ActionResult]]:
        name = application.get_namespaced_name()
        context = self.get_context(name, timestamp)
        next_state = self.new_fsm(context, timestamp).on_update(application)
        self.apply_next_state(name, next_state)
        return next_state.actions

    def on_application_delete(self, application: AnyApplication, timestamp: int) -> List[Action[ActionResult]]:
        name = application.get_namespaced_name()
        del self.contexts[name]
        return []

    def on_action_result(self, result: ActionResult, timestamp: int) -> List[Action[ActionResult]]:
        name = result.get_application_name()
        context = self.get_context(name, timestamp)
        next_state = self.new_fsm(context, timestamp).on_action_result(result)
        self.apply_next_state(name, next_state)
        return next_state.actions

    def new_fsm(self, context: SchedulingContext, timestamp: int) -> FSM:
        options = FSMOptions(
            reschedule_default_delay_seconds=DEFAULT_RESCHEDULE_DELAY_SECONDS,
            reschedule_failure_delay_seconds=DEFAULT_FAILURE_DELAY_SECONDS,
        )
        return FSM(context, self.current_zone, timestamp, options)

    def get_context(self, name: NamespacedName, timestamp: int) -> SchedulingContext:
        if name not in self.contexts:
            self.contexts[name] = SchedulingContext.new(timestamp, name, list(self.zones))

        return self.contexts[name]

    def apply_next_state(self, name: NamespacedName, next_state: NextStateResult) -> None:
        if next_state.remove_and_drop_context:
            del self.contexts[name]
        if next_state.context:
            self.contexts[name] = next_state.context

    def get_scheduling_states(self) -> List[ApplicationState]:
        results = []
        for name, context in self.contexts.items():
            history = []
            ctx: Optional[SchedulingContext] = context
            while ctx:
                entry = SchedulingEntry(
                    seq_nr=ctx.seq_nr,
                    state=str(ctx.state),
                    msg=ctx.msg,
                    running_jobs=[type(action).__name__ for action in ctx.inprogress_actions.values()],
                )
                history.append(entry)
                ctx = ctx.previous

            app_state = ApplicationState(
                name=name.name,
                namespace=name.namespace,
                history=history,
            )
            results.append(app_state)
        return results
