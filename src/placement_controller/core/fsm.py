from typing import List, Mapping

import json
from dataclasses import dataclass

from application_client import models

from placement_controller.api.model import BidCriteria, BidRequestModel, ErrorResponse, Metric
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication, GlobalState, PlacementStrategy
from placement_controller.core.context import SchedulingContext
from placement_controller.core.next_state_result import NextStateResult
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection, SchedulingState
from placement_controller.core.types import SchedulingStep
from placement_controller.jobs.bid_action import BidAction, BidActionResult, BidResponseOrError, ZoneId
from placement_controller.jobs.decision_action import DecisionAction, DecisionActionResult
from placement_controller.jobs.get_spec_action import GetSpecAction, GetSpecResult
from placement_controller.jobs.placement_action import PlacementDecision, SetPlacementAction, SetPlacementActionResult
from placement_controller.jobs.types import Action, ActionResult
from placement_controller.membership.types import PlacementZone


@dataclass
class FSMOptions:
    reschedule_default_delay_seconds: int
    reschedule_failure_delay_seconds: int


class FSM:
    ctx: SchedulingContext
    options: FSMOptions
    timestamp: int

    def __init__(
        self,
        ctx: SchedulingContext,
        timestamp: int,
        options: FSMOptions,
    ):
        self.ctx = ctx
        self.timestamp = timestamp
        self.options = options

    def on_tick(self) -> NextStateResult:
        # unmanaged state should never expire, therefore we just ignore it
        if self.ctx.state.is_valid_at(SchedulingStep.UNMANAGED, self.timestamp):
            return NextStateResult()

        if self.ctx.state.is_valid_at(SchedulingStep.PENDING, self.timestamp):
            # handling changes in the application or membership during update
            operation = self.determine_operation(self.ctx.application)
            if operation.direction == ScaleDirection.UPSCALE or operation.direction == ScaleDirection.DOWNSCALE:
                self.ctx = self.ctx.start_operation(operation, self.timestamp)
                return self.new_get_spec(self.ctx.application)

        # start over if pending is expired (optimization flow)
        if self.ctx.state.is_expired_state(SchedulingStep.PENDING, self.timestamp):
            application = self.ctx.application
            return self.on_optimize_bids(application)

        # if any other step is expired retry
        if self.ctx.state.is_expired(self.timestamp):
            return self.retry("Action timeout.")

        return NextStateResult()

    def on_update(self, application: AnyApplication) -> NextStateResult:
        placement_strategy = application.get_placement_strategy()
        global_state = application.get_global_state()
        owner_zone = application.get_owner_zone()

        is_global_placement = placement_strategy == PlacementStrategy.Global
        is_owner_current_zone = owner_zone == self.ctx.current_zone

        # switch to managed state
        if self.ctx.state.is_valid_at(SchedulingStep.UNMANAGED, self.timestamp):

            if is_owner_current_zone and is_global_placement:
                msg = "Ownership changed. Application managed."
                self.ctx = self.ctx.to_next(SchedulingStep.PENDING, self.timestamp, msg)
            else:
                # remaining unmanaged if zones are not
                next_context = self.ctx.update_application(application)
                return NextStateResult(context=next_context)

        # switch to unmanaged state
        if not is_owner_current_zone or not is_global_placement:
            placement_msg = "Local placement. " if not is_global_placement else ""
            ownership_msg = f"Ownership is assigned to {owner_zone}. " if not is_owner_current_zone else ""
            msg = placement_msg + ownership_msg + "Application unmanaged."
            next_context = self.ctx.to_next(SchedulingStep.UNMANAGED, self.timestamp, msg)
            return NextStateResult(context=next_context)

        if self.ctx.state.is_valid_at(SchedulingStep.PENDING, self.timestamp):
            if global_state == GlobalState.PlacementGlobalState:
                return self.on_placement_action(application)
            elif global_state == GlobalState.FailureGlobalState:
                return self.on_global_failure(application)

        next_context = self.ctx.update_application(application)
        return NextStateResult(context=next_context)

    def on_placement_action(self, application: AnyApplication) -> NextStateResult:
        # no action is progress
        if self.ctx.inprogress_actions_count() == 0:
            operation = self.determine_operation(application)
            if operation.direction != ScaleDirection.NONE:
                self.ctx = self.ctx.update_application(application)
                self.ctx = self.ctx.start_operation(operation, self.timestamp)
                return self.new_get_spec(application)
        return NextStateResult()

    def on_optimize_bids(self, application: AnyApplication) -> NextStateResult:
        operation = self.determine_operation(application)
        if operation.direction == ScaleDirection.UPSCALE or operation.direction == ScaleDirection.DOWNSCALE:
            return self.on_placement_action(application)
        elif operation.direction == ScaleDirection.NONE:
            self.ctx = self.ctx.start_operation(operation, self.timestamp)
            return self.new_get_spec(application)

    def on_global_failure(self, application: AnyApplication) -> NextStateResult:
        # not implemented yet, skipping for now
        # in case of failure put in a different zone
        next_context = self.ctx.update_application(application)
        return NextStateResult(context=next_context)

    def on_action_result(self, result: ActionResult) -> NextStateResult:
        if self.ctx.state.is_valid_at(SchedulingStep.UNMANAGED, self.timestamp):
            msg = f"Application is unmanaged. Ignoring action result {type(result).__name__}"
            next_context = self.ctx.to_next(SchedulingStep.UNMANAGED, self.timestamp, msg)
            return NextStateResult(context=next_context)

        if self.ctx.state.is_valid_at(SchedulingStep.FETCH_APPLICATION_SPEC, self.timestamp) and isinstance(
            result, GetSpecResult
        ):
            return self.on_get_spec_result(result)
        elif self.ctx.state.is_valid_at(SchedulingStep.BID_COLLECTION, self.timestamp) and isinstance(
            result, BidActionResult
        ):
            return self.on_bid_action_result(result)
        elif self.ctx.state.is_valid_at(SchedulingStep.DECISION, self.timestamp) and isinstance(
            result, DecisionActionResult
        ):
            return self.on_decision_action_result(result)
        elif self.ctx.state.is_valid_at(SchedulingStep.SET_PLACEMENT, self.timestamp) and isinstance(
            result, SetPlacementActionResult
        ):
            return self.on_set_placement_action_result(result)

        return NextStateResult()

    def new_get_spec(self, application: AnyApplication) -> NextStateResult:

        next_action: Action[ActionResult] = GetSpecAction(
            application.get_namespaced_name(),
            self.ctx.gen_action_id(),
        )  # type: ignore

        msg = "Getting application specification..."
        next_state = self.ctx.state.to(SchedulingStep.FETCH_APPLICATION_SPEC, self.timestamp)
        next_context = self.ctx.to_next_with_app(next_state, application, self.timestamp, msg).with_action(next_action)

        return NextStateResult(actions=[next_action], context=next_context)

    def on_get_spec_result(self, result: GetSpecResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while getting application specification. Action is not found. ")

        if isinstance(result.response, models.ApplicationSpec):
            self.ctx = self.ctx.with_application_spec(
                action.action_id,
                result.response,
                self.timestamp,
                "Application spec fetched successfully.",
            )
            msg = "Starting bidding..."
            return self.new_bid_action(result.response, result.get_application_name(), msg)
        else:
            error: ErrorResponse = result.response
            return self.retry(f"Failure while getting application specification. {error.msg} ")

    def new_bid_action(self, spec: models.ApplicationSpec, name: NamespacedName, msg: str) -> NextStateResult:
        operation = self.ctx.state.operation
        if not operation:
            return self.placement_failure("FSMOperation is not set in context. Invariant failure. Programmer mistake!")

        spec_str = json.dumps(spec.to_dict())
        bid_criteria = [BidCriteria.cpu, BidCriteria.memory]
        metrics = {Metric.cost, Metric.energy}

        bid = BidRequestModel(id=self.ctx.gen_action_id(), spec=spec_str, bid_criteria=bid_criteria, metrics=metrics)

        next_action: Action[ActionResult] = BidAction(operation, bid, name)  # type: ignore
        next_context = self.ctx.to_next(SchedulingStep.BID_COLLECTION, self.timestamp, msg).with_action(next_action)

        return NextStateResult(actions=[next_action], context=next_context)

    def on_bid_action_result(self, result: BidActionResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while receiving bids. Action is not found. ")
        response_str = bid_response_to_human_readable(result.response)

        if result.is_success():
            msg = f"Bids received. {response_str}"
            self.ctx = self.ctx.with_bid_responses(
                action.action_id,
                result.response,
                self.timestamp,
                msg,
            )
            return self.new_decision_action(result.response, result.get_application_name(), msg)
        else:
            return self.retry(f"Failure while receiving bids. {response_str} ")

    def new_decision_action(
        self,
        bids: Mapping[ZoneId, BidResponseOrError],
        name: NamespacedName,
        msg: str,
    ) -> NextStateResult:
        operation = self.ctx.state.operation
        if not operation:
            return self.placement_failure("FSMOperation is not set in context. Invariant failure. Programmer mistake!")

        next_action: Action[ActionResult] = DecisionAction(
            bids, operation, name, self.ctx.gen_action_id()
        )  # type: ignore
        next_context = self.ctx.to_next(SchedulingStep.DECISION, self.timestamp, msg).with_action(next_action)
        return NextStateResult(actions=[next_action], context=next_context)

    def on_decision_action_result(self, result: DecisionActionResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while making placements decision. Action is not found. ")

        if isinstance(result.result, list):
            self.ctx = self.ctx.with_placement_decision(
                action.action_id,
                result.result,
                self.timestamp,
                "Decision is made.",
            )
            msg = "Setting placements..."
            return self.new_set_placement_action(result.result, result.get_application_name(), msg)
        else:
            error: ErrorResponse = result.result
            return self.retry(f"Failure while setting placements. {error.msg} ")

    def new_set_placement_action(
        self,
        placements: List[PlacementZone],
        name: NamespacedName,
        msg: str,
    ) -> NextStateResult:
        if not self.ctx.application_spec:
            return self.placement_failure("Unable to create placement action. Lifecycle error. Programmer mistake!")
        spec = json.dumps(self.ctx.application_spec.to_dict())
        decision = PlacementDecision(
            spec=spec,
            placements=placements,
            reason=self.ctx.reason or "reason is not set",
            trace=self.ctx.trace.get_data(),
        )
        next_action: Action[ActionResult] = SetPlacementAction(decision, name, self.ctx.gen_action_id())  # type: ignore
        next_context = self.ctx.to_next(SchedulingStep.SET_PLACEMENT, self.timestamp, msg).with_action(next_action)
        return NextStateResult(actions=[next_action], context=next_context)

    def on_set_placement_action_result(self, result: SetPlacementActionResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while setting placements. Action is not found. ")

        if isinstance(result.result, bool):
            self.ctx = self.ctx.with_placements_done(action.action_id, self.timestamp, "Placements done.")

            expires_at = self.timestamp + self.options.reschedule_default_delay_seconds * 1000
            next_state = SchedulingState.new(SchedulingStep.PENDING, expires_at)

            msg = "Switched to Pending."
            next_context = self.ctx.to_next_with_app(next_state, self.ctx.application, self.timestamp, msg)
            next_context.reset()
            return NextStateResult(context=next_context)
        else:
            error: ErrorResponse = result.result
            return self.retry(f"Failure while receiving bids specification. {error.msg} ")

    def retry(self, msg: str) -> NextStateResult:
        if not self.ctx.is_attempts_exhausted():
            next_context = self.ctx.retry(self.timestamp, msg + "Retrying...")
            actions = list(self.ctx.inprogress_actions.values())
            return NextStateResult(context=next_context, actions=actions)
        else:
            return self.placement_failure(msg + "All attempts exhausted.")

    def placement_failure(self, msg: str) -> NextStateResult:
        expires_at = self.timestamp + self.options.reschedule_failure_delay_seconds * 1000
        next_state = SchedulingState.new(SchedulingStep.PENDING, expires_at)
        next_context = self.ctx.to_next_with_app(next_state, None, self.timestamp, msg)
        next_context.inprogress_actions = dict()
        return NextStateResult(context=next_context)

    def on_membership_change(self, available_zones: List[PlacementZone]) -> NextStateResult:

        zone_names = ",".join([zone.id for zone in available_zones])
        msg = f"Membership update: Available zones '{zone_names}'"

        self.ctx = self.ctx.to_next(self.ctx.state.step, self.timestamp, msg).with_available_zones(available_zones)

        if self.ctx.state.is_valid_at(SchedulingStep.UNMANAGED, self.timestamp):
            return NextStateResult(context=self.ctx)

        # check if zone is failed
        application = self.ctx.application
        operation = self.determine_operation(application)
        if operation.direction != ScaleDirection.NONE:
            self.ctx = self.ctx.start_operation(operation, self.timestamp)
            return self.new_get_spec(application)

        return NextStateResult(context=self.ctx)

    def determine_operation(self, application: AnyApplication) -> FSMOperation:
        desired_replica = application.get_desired_replica()
        current_placement_zones = set(application.get_placement_zones())
        available_zones = {zone.id for zone in self.ctx.available_zones}

        current_active_zones = set(current_placement_zones)
        unavailable_zones = current_placement_zones - available_zones
        active_zones = current_active_zones - unavailable_zones

        # underprovisioned
        if desired_replica > len(active_zones):
            # check the posibility of upscaling
            if len(available_zones) > len(active_zones):
                return FSMOperation(
                    direction=ScaleDirection.UPSCALE,
                    required_replica=desired_replica,
                    current_zones=current_placement_zones,
                    available_zones=available_zones,
                )
        # overprovisioned
        elif desired_replica < len(active_zones):
            return FSMOperation(
                direction=ScaleDirection.DOWNSCALE,
                required_replica=desired_replica,
                current_zones=current_placement_zones,
                available_zones=available_zones,
            )
        return FSMOperation(
            direction=ScaleDirection.NONE,
            required_replica=desired_replica,
            current_zones=current_placement_zones,
            available_zones=available_zones,
        )


def bid_response_to_human_readable(bid_response: Mapping[ZoneId, BidResponseOrError]) -> str:
    response_str = ""
    sep = ""
    for zone, response in bid_response.items():
        response_str += sep + f"zone {zone}: " + response.to_human_readable()
        sep = ", "
    return response_str
