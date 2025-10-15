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
from placement_controller.jobs.placement_action import SetPlacementAction, SetPlacementActionResult
from placement_controller.jobs.types import Action, ActionResult
from placement_controller.membership.types import PlacementZone

# TODO: ticker timeout
#   - retry after timeout
#       - drop context
#       - set retry timeout

# TODO: optimization bids
#   - confirm bids periodically and change placements
#       - bid zones
#       - upscale and downscale
#           - drop the worst, add the best
#           - set retry timeout

# TODO: membership change partial schedule
#   - upscale:
#       - bid zones
#       - add the best
#   - downscale:
#       - bid zones
#       - drop the worst

# TODO: spec update partial schedule
#   - upscale:
#       - bid zones
#       - add the best
#   - downscale:
#       - drop the worst

# TODO: zone failure (membership change) and convergence
#   - failure
#       - upscale
#           - bid zones
#           - add the best
#   - convergence:
#       - downscale
#           - bid zones
#           - drop the worst


@dataclass
class FSMOptions:
    reschedule_default_delay_seconds: int
    reschedule_failure_delay_seconds: int


class FSM:
    ctx: SchedulingContext
    options: FSMOptions
    current_zone: str
    timestamp: int

    def __init__(
        self,
        ctx: SchedulingContext,
        current_zone: str,
        timestamp: int,
        options: FSMOptions,
    ):
        self.ctx = ctx
        self.timestamp = timestamp
        self.current_zone = current_zone
        self.options = options

    def on_tick(self) -> NextStateResult:
        # if state does not exists treat it as application update
        # check managed unmanaged

        if self.ctx.state.is_expired(self.timestamp):
            return self.retry("Action timeout.")
        return NextStateResult()

    def determine_operation(self, application: AnyApplication) -> FSMOperation:
        desired_replica = application.get_desired_replica()
        current_placement_zones = set(application.get_placement_zones())
        available_zones = {zone.id for zone in self.ctx.available_zones}

        # TODO check zone failure

        # underprovisioned
        if desired_replica > len(current_placement_zones):
            # check the posibility of upscaling
            if len(available_zones) > len(current_placement_zones):
                return FSMOperation(
                    direction=ScaleDirection.UPSCALE,
                    required_replica=desired_replica,
                    current_zones=current_placement_zones,
                    available_zones=available_zones,
                )
        # overprovisioned
        elif desired_replica < len(current_placement_zones):
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

    def on_update(self, application: AnyApplication) -> NextStateResult:
        placement_strategy = application.get_placement_strategy()
        global_state = application.get_global_state()
        owner_zone = application.get_owner_zone()

        # if current zone is not the owner -> ignore (or drop scheduling context if it is valid)
        if owner_zone != self.current_zone:
            if self.ctx.state.is_valid_at(SchedulingStep.PENDING, self.timestamp):
                # TODO since it is update -> update application in context
                # TODO update to unmanaged instead of remove
                return NextStateResult(remove_and_drop_context=True)
            else:
                # TODO since it is update -> update application in context
                return NextStateResult()

        # Placement strategy is local -> ignore (or drop scheduling context if it is valid)
        if placement_strategy == PlacementStrategy.Local:
            if self.ctx.state.is_valid_at(SchedulingStep.PENDING, self.timestamp):
                # TODO since it is update -> update application in context
                # TODO update to unmanaged instead of remove
                return NextStateResult(remove_and_drop_context=True)
            else:
                # TODO since it is update -> update application in context
                return NextStateResult()

        if global_state == GlobalState.PlacementGlobalState:
            return self.on_placement_action(application)
        elif global_state == GlobalState.FailureGlobalState:
            return self.on_global_failure(application)

        # TODO since it is update -> update application in context
        return NextStateResult()

    def on_placement_action(self, application: AnyApplication) -> NextStateResult:
        if self.ctx.state.is_valid_at(SchedulingStep.PENDING, self.timestamp):
            # no action is progress
            if self.ctx.inprogress_actions_count() == 0:
                operation = self.determine_operation(application)
                if operation.direction != ScaleDirection.NONE:

                    self.ctx = self.ctx.start_operation(operation, application, self.timestamp)
                    return self.new_get_spec(application)

        # TODO update application in context
        return NextStateResult()

    def on_global_failure(self, application: AnyApplication) -> NextStateResult:
        # not implemented yet, skipping for now
        # in case of failure put in a different zone
        # TODO since it is update -> update application in context
        return NextStateResult()

    def on_action_result(self, result: ActionResult) -> NextStateResult:
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

        spec_str = json.dumps(spec.to_dict())
        zones = [zone.id for zone in self.ctx.available_zones]
        bid_criteria = [BidCriteria.cpu, BidCriteria.memory]
        metrics = {Metric.cost, Metric.energy}

        bid = BidRequestModel(id=self.ctx.gen_action_id(), spec=spec_str, bid_criteria=bid_criteria, metrics=metrics)

        next_action: Action[ActionResult] = BidAction(set(zones), self.ctx.operation, bid, name)  # type: ignore
        next_context = self.ctx.to_next(SchedulingStep.BID_COLLECTION, self.timestamp, msg).with_action(next_action)

        return NextStateResult(actions=[next_action], context=next_context)

    def on_bid_action_result(self, result: BidActionResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while receiving bids. Action is not found. ")

        if result.is_success():
            application = self.ctx.application
            if not application:
                return self.placement_failure(
                    "Application is not set in context. Invariant failure. Programmer mistake!"
                )
            self.ctx = self.ctx.with_bid_responses(
                action.action_id,
                result.response,
                self.timestamp,
                "Bids received.",
            )
            msg = "Making decision..."
            return self.new_decision_action(application, result.response, result.get_application_name(), msg)
        else:
            return self.retry(f"Failure while receiving bids. {result.response} ")  # TODO stringify error

    def new_decision_action(
        self,
        application: AnyApplication,
        bids: Mapping[ZoneId, BidResponseOrError],
        name: NamespacedName,
        msg: str,
    ) -> NextStateResult:
        next_action: Action[ActionResult] = DecisionAction(bids, name, self.ctx.gen_action_id())  # type: ignore
        next_context = self.ctx.to_next(SchedulingStep.DECISION, self.timestamp, msg).with_action(next_action)
        return NextStateResult(actions=[next_action], context=next_context)

    def on_decision_action_result(self, result: DecisionActionResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while making placements decision. Action is not found. ")

        if isinstance(result.result, list):
            application = self.ctx.application
            if not application:
                return self.placement_failure(
                    "Application is not set in context. Invariant failure. Programmer mistake!"
                )
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
        next_action: Action[ActionResult] = SetPlacementAction(
            placements, name, self.ctx.gen_action_id()
        )  # type: ignore
        next_context = self.ctx.to_next(SchedulingStep.SET_PLACEMENT, self.timestamp, msg).with_action(next_action)
        return NextStateResult(actions=[next_action], context=next_context)

    def on_set_placement_action_result(self, result: SetPlacementActionResult) -> NextStateResult:
        action = self.ctx.get_action_by_id(result.action_id)
        if not action:
            return self.placement_failure("Failure while setting placements. Action is not found. ")

        if isinstance(result.result, bool):
            application = self.ctx.application
            if not application:
                return self.placement_failure(
                    "Application is not set in context. Invariant failure. Programmer mistake!"
                )

            # in the end we check if we should start operation again
            operation = self.determine_operation(application)
            if operation.direction != ScaleDirection.NONE:
                self.ctx = self.ctx.start_operation(operation, application, self.timestamp)
                return self.new_get_spec(application)

            # TODO check unmanaged
            expires_at = self.timestamp + self.options.reschedule_default_delay_seconds * 1000
            next_state = SchedulingState.new(SchedulingStep.PENDING, expires_at)
            msg = "Placement done."
            next_context = self.ctx.to_next_with_app(next_state, None, self.timestamp, msg)
            return NextStateResult(context=next_context)
        else:
            error: ErrorResponse = result.result
            return self.retry(f"Failure while receiving bids specification. {error.msg} ")

    def retry(self, msg: str) -> NextStateResult:
        if not self.ctx.is_attempts_exhausted():
            next_context = self.ctx.retry(self.timestamp, msg + "Retrying...")
            return NextStateResult(context=next_context)
        else:
            return self.placement_failure(msg + "All attempts exhausted.")

    def placement_failure(self, msg: str) -> NextStateResult:
        expires_at = self.timestamp + self.options.reschedule_failure_delay_seconds * 1000
        next_state = SchedulingState.new(SchedulingStep.PENDING, expires_at)
        next_context = self.ctx.to_next_with_app(next_state, None, self.timestamp, msg)
        return NextStateResult(context=next_context)

    def on_membership_change(self, available_zones: List[PlacementZone]) -> NextStateResult:

        zone_names = ",".join([zone.id for zone in available_zones])
        msg = f"Placement changed to '{zone_names}'"

        self.ctx = self.ctx.to_next(self.ctx.state.step, self.timestamp, msg).with_available_zones(available_zones)

        # check if zone is failed
        application = self.ctx.application
        if application is not None:
            operation = self.determine_operation(application)
            if operation.direction != ScaleDirection.NONE:
                self.ctx = self.ctx.start_operation(operation, application, self.timestamp)
                return self.new_get_spec(application)

        return NextStateResult(context=self.ctx)
