import unittest
from decimal import Decimal

from application_client import models

from placement_controller.api.model import BidResponseModel, BidStatus, Metric, MetricUnit, MetricValue
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM
from placement_controller.core.types import SchedulingState
from placement_controller.jobs.bid_action import BidActionResult
from placement_controller.jobs.decision_action import DecisionActionResult
from placement_controller.jobs.get_spec_action import GetSpecResult
from placement_controller.jobs.placement_action import SetPlacementActionResult
from placement_controller.membership.types import PlacementZone
from placement_controller.resource_fixture import ResourceTestFixture


class FSMTest(unittest.TestCase, ResourceTestFixture):

    name: NamespacedName
    application: AnyApplication
    spec: models.ApplicationSpec
    response1: BidResponseModel
    response2: BidResponseModel

    def setUp(self) -> None:
        self.name = NamespacedName(name="test", namespace="test")
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
        # NEW state
        context = SchedulingContext.new(1, [])
        self.assertEqual(context.state, SchedulingState.NEW)

        # FETCH_APPLICATION_SPEC
        result = FSM(context, 1).next_state(self.application)

        context = result.context  # type: ignore
        self.assertEqual(context.state, SchedulingState.FETCH_APPLICATION_SPEC)

        get_spec = result.actions[0]
        self.assertEqual(get_spec.name, self.name)

        # BID_COLLECTION
        get_spec_result = GetSpecResult(self.spec, self.name, get_spec.action_id)
        result = FSM(context, 2).on_action_result(get_spec_result)

        context = result.context  # type: ignore
        self.assertEqual(context.state, SchedulingState.BID_COLLECTION)

        bid_action = result.actions[0]
        self.assertEqual(bid_action.name, self.name)

        # DECISION
        bid_responses = {"zone1": self.response1, "zone2": self.response2}
        bid_action_result = BidActionResult(bid_responses, self.name, bid_action.action_id)
        result = FSM(context, 3).on_action_result(bid_action_result)

        context = result.context  # type: ignore
        self.assertEqual(context.state, SchedulingState.DECISION)

        decision_action = result.actions[0]
        self.assertEqual(decision_action.name, self.name)

        # SET_PLACEMENT
        decision_result = DecisionActionResult(self.placements, self.name, decision_action.action_id)
        result = FSM(context, 4).on_action_result(decision_result)

        context = result.context  # type: ignore
        self.assertEqual(context.state, SchedulingState.SET_PLACEMENT)

        set_placement_action = result.actions[0]
        self.assertEqual(set_placement_action.name, self.name)

        # DONE
        set_placement_result = SetPlacementActionResult(True, self.name, set_placement_action.action_id)
        result = FSM(context, 5).on_action_result(set_placement_result)

        context = result.context  # type: ignore
        self.assertEqual(context.state, SchedulingState.DONE)


# TODO more tests covering application update during scheduling
