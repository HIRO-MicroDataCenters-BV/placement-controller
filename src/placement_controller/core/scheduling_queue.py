from typing import Dict, Optional

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.jobs.types import Action, ActionResult


class SchedulingQueue:
    applications: Dict[NamespacedName, SchedulingContext]

    def __init__(self):
        self.applications = dict()

    def on_update(self, application: AnyApplication) -> Optional[Action[ActionResult]]:
        # name = application.get_namespaced_name()
        return None

    def on_delete(self, application: AnyApplication) -> Optional[Action[ActionResult]]:
        name = application.get_namespaced_name()
        del self.applications[name]
        return None

    def on_action_result(self, result: ActionResult) -> Optional[Action[ActionResult]]:
        return None
