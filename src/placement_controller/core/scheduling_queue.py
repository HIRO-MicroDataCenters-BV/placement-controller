from typing import Dict, Optional

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM
from placement_controller.core.types import SchedulingState
from placement_controller.jobs.types import Action, ActionResult
from placement_controller.membership.types import Membership


class SchedulingQueue:
    contexts: Dict[NamespacedName, SchedulingContext]

    def __init__(self):
        self.contexts = dict()

    def on_membership_update(self, membership: Membership) -> Optional[Action[ActionResult]]:
        return None

    def on_application_update(self, application: AnyApplication) -> Optional[Action[ActionResult]]:
        name = application.get_namespaced_name()
        if name not in self.contexts:
            self.contexts[name] = SchedulingContext(SchedulingState.NEW, application)

        context = self.contexts[name]
        fsm = FSM()
        next_state_result = fsm.next_state(context, application)

        print(next_state_result)
        return None

    def on_application_delete(self, application: AnyApplication) -> Optional[Action[ActionResult]]:
        name = application.get_namespaced_name()
        del self.contexts[name]
        return None

    def on_action_result(self, result: ActionResult) -> Optional[Action[ActionResult]]:
        # name = result.get_application_name()
        return None
