from typing import Dict

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.jobs.types import ActionResult


class SchedulingQueue:
    applications: Dict[NamespacedName, SchedulingContext]

    def __init__(self):
        self.applications = dict()

    def on_update(self, application: AnyApplication) -> None:
        pass

    def on_delete(self, application: AnyApplication) -> None:
        pass

    def on_action_result(self, result: ActionResult) -> None:
        pass
