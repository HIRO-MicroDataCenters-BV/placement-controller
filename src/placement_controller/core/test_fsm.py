from typing import Any, Dict, List, Optional, Type

import copy
import unittest
from decimal import Decimal

from application_client import models

from placement_controller.api.model import BidResponseModel, BidStatus, Metric, MetricUnit, MetricValue
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import DEFAULT_ACTION_TIMEOUT_SECONDS, SchedulingContext
from placement_controller.core.fsm import FSM, FSMOptions
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection, SchedulingState
from placement_controller.core.types import SchedulingStep
from placement_controller.jobs.bid_action import BidAction, BidActionResult
from placement_controller.jobs.decision_action import DecisionAction, DecisionActionResult
from placement_controller.jobs.get_spec_action import GetSpecAction, GetSpecResult
from placement_controller.jobs.placement_action import SetPlacementAction, SetPlacementActionResult
from placement_controller.membership.types import PlacementZone
from placement_controller.resource_fixture import ResourceTestFixture


class FSMTest(unittest.TestCase, ResourceTestFixture):

    options: FSMOptions
    now: int
    name: NamespacedName
    application: AnyApplication
    spec: models.ApplicationSpec
    response1: BidResponseModel
    response2: BidResponseModel
    response3: BidResponseModel

    def setUp(self) -> None:
        self.now = 0
        self.options = FSMOptions(
            reschedule_default_delay_seconds=10,
            reschedule_failure_delay_seconds=20,
        )
        self.name = NamespacedName(name="test", namespace="test")
        self.current_zone = "zone1"
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", [])
        )

        self.spec = models.ApplicationSpec(
            id=models.ResourceId(name=self.name.name, namespace=self.name.namespace),
            resources=[self.make_pod_spec("pod1", 1, {"cpu": "2", "memory": "200Mi"}, {})],
        )

        self.response1 = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.01"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )
        self.response2 = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.03"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )
        self.response3 = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.05"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )

    def test_ordinary_placement(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", [])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=1,
            current_zones=set(),
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")], 60000)

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_upscale(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 60000
        )

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_downscale(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", ["zone1", "zone2"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.DOWNSCALE,
            required_replica=1,
            current_zones={"zone1", "zone2"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")], 60000)

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_zone_failure(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1", "zone2"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1", "zone2"},
            available_zones={"zone2", "zone3"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone2"), PlacementZone(id="zone3")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone2": self.response2, "zone3": self.response3}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone2"), PlacementZone(id="zone3")], 60000
        )

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_converge_after_failure(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response2, "zone2": self.response3}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 60000
        )

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_action_timeouts_and_retries(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", [])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=1,
            current_zones=set(),
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)
        context = self.assert_retry(context, SchedulingStep.FETCH_APPLICATION_SPEC, operation, GetSpecAction)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 120001)
        context = self.assert_retry(context, SchedulingStep.BID_COLLECTION, operation, BidAction)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 180002
        )
        context = self.assert_retry(context, SchedulingStep.DECISION, operation, DecisionAction)

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")], 240003)
        context = self.assert_retry(context, SchedulingStep.SET_PLACEMENT, operation, SetPlacementAction)

        # PENDING
        self.assert_placements_done(context, 250004)

    # def test_action_retries_and_failures(self) -> None:
    #     pass

    # def test_optimize_periodically(self) -> None:
    #     pass

    # def test_unmanaged(self) -> None:
    #     pass

    def test_update_during_operation(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)
        self.assert_application_update(context, SchedulingStep.FETCH_APPLICATION_SPEC, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)
        self.assert_application_update(context, SchedulingStep.BID_COLLECTION, operation)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )
        self.assert_application_update(context, SchedulingStep.DECISION, operation)

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 60000
        )
        self.assert_application_update(context, SchedulingStep.SET_PLACEMENT, operation)

        # PENDING
        context = self.assert_placements_done(context, 10000)

        operation.required_replica = 3
        self.assert_application_update(context, SchedulingStep.FETCH_APPLICATION_SPEC, operation)

    def assert_fetch_application_spec(
        self,
        context: SchedulingContext,
        operation: FSMOperation,
    ) -> SchedulingContext:
        result = FSM(context, self.current_zone, self.now, self.options).on_update(self.application)

        if result.context is None:
            self.fail("context expected")

        context = result.context
        self.assertEqual(
            context.state,
            SchedulingState(
                SchedulingStep.FETCH_APPLICATION_SPEC,
                60000,
                operation,
            ),
        )

        get_spec = result.actions[0]
        self.assertEqual(get_spec.name, self.name)
        return context

    def assert_get_spec_to_bid_collection(
        self, context: SchedulingContext, operation: FSMOperation, state_ts: int
    ) -> SchedulingContext:
        action = context.get_action_by_type(GetSpecAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        get_spec_result = GetSpecResult(self.spec, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(get_spec_result)

        if result.context is None:
            self.fail("context expected")

        context = result.context
        expected_state = SchedulingState(SchedulingStep.BID_COLLECTION, state_ts, operation)
        self.assertEqual(
            context.state,
            expected_state,
            f"expected state {expected_state} actual {context.state}",
        )

        bid_action = result.actions[0]
        self.assertEqual(bid_action.name, self.name)

        return context

    def assert_bid_collection_to_decision(
        self,
        context: SchedulingContext,
        operation: FSMOperation,
        bid_responses: Dict[str, BidResponseModel],
        state_ts: int,
    ) -> SchedulingContext:
        action = context.get_action_by_type(BidAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        bid_action_result = BidActionResult(bid_responses, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(bid_action_result)

        if result.context is None:
            self.fail("context expected")

        context = result.context

        expected_state = SchedulingState(SchedulingStep.DECISION, state_ts, operation)
        self.assertEqual(
            context.state,
            expected_state,
            f"expected state {expected_state} actual {context.state}",
        )

        decision_action = result.actions[0]
        self.assertEqual(decision_action.name, self.name)

        return context

    def assert_decision_to_placement(
        self,
        context: SchedulingContext,
        operation: FSMOperation,
        placements: List[PlacementZone],
        state_ts: int,
    ) -> SchedulingContext:
        action = context.get_action_by_type(DecisionAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        decision_result = DecisionActionResult(placements, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(decision_result)

        if result.context is None:
            self.fail("context expected")
        context = result.context
        expected_state = SchedulingState(SchedulingStep.SET_PLACEMENT, state_ts, operation)
        self.assertEqual(
            context.state,
            expected_state,
            f"expected state {expected_state} actual {context.state}",
        )

        set_placement_action: SetPlacementAction = result.actions[0]  # type: ignore
        self.assertEqual(set_placement_action.name, self.name)
        self.assertEqual(set_placement_action.zones, placements)

        return context

    def assert_placements_done(self, context: SchedulingContext, state_ts: int) -> SchedulingContext:
        action = context.get_action_by_type(SetPlacementAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        set_placement_result = SetPlacementActionResult(True, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(set_placement_result)

        if result.context is None:
            self.fail("context expected")

        context = result.context

        expected_state = SchedulingState.new(SchedulingStep.PENDING, state_ts)
        self.assertEqual(
            context.state,
            expected_state,
            f"expected state {expected_state} actual {context.state}",
        )
        return context

    def assert_retry(
        self,
        context: SchedulingContext,
        step: SchedulingStep,
        operation: FSMOperation,
        action_type: Type[Any],
    ) -> SchedulingContext:
        self.now += DEFAULT_ACTION_TIMEOUT_SECONDS * 1000 + 1
        result = FSM(context, self.current_zone, self.now, self.options).on_tick()

        if result.context is None:
            self.fail("context expected")

        context = result.context
        self.assertEqual(context.state.step, step)
        self.assertEqual(context.state.operation, operation)
        self.assertEqual(type(result.actions.pop()), action_type)
        return context

    def assert_application_update(
        self,
        context: SchedulingContext,
        step: SchedulingStep,
        operation: Optional[FSMOperation],
    ) -> SchedulingContext:
        if context.application is None:
            self.fail("application expected")

        updated_app = copy.deepcopy(context.application)
        updated_app.object["spec"]["zones"] += 1

        result = FSM(context, self.current_zone, self.now, self.options).on_update(updated_app)

        if result.context is None:
            self.fail("context expected")
        context = result.context

        if context.application is None:
            self.fail("application expected")

        self.assertEqual(context.application.object, updated_app.object)
        self.assertEqual(context.state.step, step)
        self.assertEqual(context.state.operation, operation)
        return context
