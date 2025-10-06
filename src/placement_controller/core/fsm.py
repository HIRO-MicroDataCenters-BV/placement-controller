from typing import List

from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.jobs.types import Action, ActionResult


class NextStateResult:
    actions: List[Action]


class FSM:
    application: AnyApplication

    def __init__(self, application: AnyApplication):
        self.application = application

    def next_state(self, context: SchedulingContext) -> NextStateResult:
        return NextStateResult()

    def on_action_result(self, result: ActionResult) -> NextStateResult:
        return NextStateResult()
