from typing import Set

from placement_controller.core.application import AnyApplication, GlobalState
from placement_controller.core.context import SchedulingContext
from placement_controller.core.next_state_result import NextStateResult
from placement_controller.core.types import SchedulingState
from placement_controller.jobs.bid_action import BidActionResult
from placement_controller.jobs.get_spec_action import GetSpecAction, GetSpecResult
from placement_controller.jobs.types import Action, ActionResult
from placement_controller.membership.types import PlacementZone


class FSM:
    ctx: SchedulingContext
    timestamp: int

    def __init__(self, ctx: SchedulingContext, timestamp: int):
        self.ctx = ctx
        self.timestamp = timestamp

    def on_tick(self) -> NextStateResult:
        return NextStateResult()

    def next_state(self, application: AnyApplication) -> NextStateResult:
        global_state = application.get_global_state()
        if global_state == GlobalState.PlacementGlobalState:
            return self.on_placement(application)
        elif global_state == GlobalState.FailureGlobalState:
            return self.on_failure(application)
        else:
            return NextStateResult()

    def on_placement(self, application: AnyApplication) -> NextStateResult:
        if self.ctx.state == SchedulingState.NEW and self.ctx.inprogress_actions_count() == 0:
            action: Action[ActionResult] = GetSpecAction(
                application.get_namespaced_name(), "action id todo"
            )  # type: ignore
            next_context = self.ctx.to_next(
                SchedulingState.FETCH_APPLICATION_SPEC, self.timestamp, "Application spec fetched successfully"
            ).with_action(action)

            return NextStateResult(actions=[action], context=next_context)

        return NextStateResult()

    def on_failure(self, application: AnyApplication) -> NextStateResult:
        return NextStateResult()

    def on_action_result(self, result: ActionResult) -> NextStateResult:
        if self.ctx.state == SchedulingState.BID_COLLECTION and isinstance(result, BidActionResult):
            action = self.ctx.get_action_by_id(result.action_id)
            if action:
                if result.is_success():
                    next_context = self.ctx.to_next(
                        SchedulingState.DECISION, self.timestamp, "Application spec fetched successfully"
                    )
                    # action = decision action
                    return NextStateResult(actions=[], context=next_context)
                else:
                    # action failure case
                    pass
            else:
                if not self.ctx.is_attempts_exhausted():
                    next_context = self.ctx.retry(
                        self.timestamp, "Get Spec failure. Retrying..."
                    )  # TODO attempt number
                else:
                    # no more attempts
                    pass

        elif self.ctx.state == SchedulingState.FETCH_APPLICATION_SPEC and isinstance(result, GetSpecResult):
            action = self.ctx.get_action_by_id(result.action_id)
            if action:
                if result.is_success():
                    next_context = self.ctx.to_next(
                        SchedulingState.BID_COLLECTION, self.timestamp, "Application spec fetched successfully"
                    )
                    # action = bid collection action
                    return NextStateResult(actions=[], context=next_context)
                else:
                    # action failure case
                    pass
            else:
                if not self.ctx.is_attempts_exhausted():
                    next_context = self.ctx.retry(
                        self.timestamp, "Get Spec failure. Retrying..."
                    )  # TODO attempt number
                else:
                    # no more attempts
                    pass

        return NextStateResult()

    def on_membership_change(self, zones: Set[PlacementZone]) -> NextStateResult:
        # ignore membership updates for now
        return NextStateResult()

        # if application.get_owner_zone() == self.settings.current_zone:
        #     if application.get_global_state() == "Placement":
        #         spec = application.get_spec()
        #         strategy = spec.get("placementStrategy") or {}
        #         if strategy.get("strategy") == "Global":
        #             # setting default placement zone to current
        #             if len(application.get_placement_zones()) == 0:
        #                 zones = [self.settings.current_zone]
        #                 name = application.get_namespaced_name()
        #                 application.set_placement_zones(zones)
        #                 await self.client.patch_status(AnyApplication.GVK, name, application.get_status_or_fail())
        #                 logger.info(f"{name} setting placement zones {zones}")
