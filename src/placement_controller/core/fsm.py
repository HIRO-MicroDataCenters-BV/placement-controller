from typing import Set

from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.next_state_result import NextStateResult
from placement_controller.jobs.types import ActionResult
from placement_controller.membership.types import PlacementZone


class FSM:

    def __init__(self):
        pass

    def next_state(self, context: SchedulingContext, application: AnyApplication) -> NextStateResult:
        return NextStateResult()

    def on_action_result(self, context: SchedulingContext, result: ActionResult) -> NextStateResult:
        return NextStateResult()

    def on_membership_change(self, context: SchedulingContext, zones: Set[PlacementZone]) -> NextStateResult:
        return NextStateResult()
