from typing import List

from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.jobs.types import Action, ActionResult


class NextStateResult:
    actions: List[Action[ActionResult]]


class FSM:

    def __init__(self):
        pass

    def next_state(self, context: SchedulingContext, application: AnyApplication) -> NextStateResult:
        return NextStateResult()

    def on_action_result(self, result: ActionResult) -> NextStateResult:
        return NextStateResult()
