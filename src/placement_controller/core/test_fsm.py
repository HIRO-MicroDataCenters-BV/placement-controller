from typing import Dict, List

import unittest
from decimal import Decimal

from application_client import models

from placement_controller.api.model import BidResponseModel, BidStatus, Metric, MetricUnit, MetricValue
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
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
        self.placements = [PlacementZone(id="zone1")]

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
        context = self.assert_get_spec_to_bid_collection(context, operation)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")])

        # PENDING
        self.assert_placements_done(context)

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
        context = self.assert_get_spec_to_bid_collection(context, operation)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )

        # PENDING
        self.assert_placements_done(context)

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
        context = self.assert_get_spec_to_bid_collection(context, operation)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")])

        # PENDING
        self.assert_placements_done(context)

    # def test_action_retries(self) -> None:
    #     # TODO tests with retries
    #     pass

    # def test_action_timeouts(self) -> None:
    #     pass

    # def test_optimize_periodically(self) -> None:
    #     pass

    # def test_zone_failure(self) -> None:
    #     pass

    # def test_converge_after_failure(self) -> None:
    #     pass

    # def test_unmanaged(self) -> None:
    #     pass

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
        self, context: SchedulingContext, operation: FSMOperation
    ) -> SchedulingContext:
        action = context.get_action_by_type(GetSpecAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        get_spec_result = GetSpecResult(self.spec, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(get_spec_result)

        if result.context is None:
            self.fail("context expected")

        context = result.context
        self.assertEqual(context.state, SchedulingState(SchedulingStep.BID_COLLECTION, 60000, operation))

        bid_action = result.actions[0]
        self.assertEqual(bid_action.name, self.name)

        return context

    def assert_bid_collection_to_decision(
        self,
        context: SchedulingContext,
        operation: FSMOperation,
        bid_responses: Dict[str, BidResponseModel],
    ) -> SchedulingContext:
        action = context.get_action_by_type(BidAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        bid_action_result = BidActionResult(bid_responses, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(bid_action_result)

        if result.context is None:
            self.fail("context expected")

        context = result.context
        self.assertEqual(context.state, SchedulingState(SchedulingStep.DECISION, 60000, operation))

        decision_action = result.actions[0]
        self.assertEqual(decision_action.name, self.name)

        return context

    def assert_decision_to_placement(
        self,
        context: SchedulingContext,
        operation: FSMOperation,
        placements: List[PlacementZone],
    ) -> SchedulingContext:
        action = context.get_action_by_type(DecisionAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        decision_result = DecisionActionResult(placements, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(decision_result)

        if result.context is None:
            self.fail("context expected")
        context = result.context
        self.assertEqual(context.state, SchedulingState(SchedulingStep.SET_PLACEMENT, 60000, operation))

        set_placement_action: SetPlacementAction = result.actions[0]  # type: ignore
        self.assertEqual(set_placement_action.name, self.name)
        self.assertEqual(set_placement_action.zones, placements)

        return context

    def assert_placements_done(self, context: SchedulingContext) -> SchedulingContext:
        action = context.get_action_by_type(SetPlacementAction)  # type: ignore
        if action is None:
            self.fail("action expected")

        set_placement_result = SetPlacementActionResult(True, self.name, action.get_id())
        result = FSM(context, self.current_zone, self.now, self.options).on_action_result(set_placement_result)

        if result.context is None:
            self.fail("context expected")

        context = result.context
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.PENDING, 10000))
        return context
