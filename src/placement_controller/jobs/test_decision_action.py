from typing import Dict

from decimal import Decimal

from placement_controller.api.model import BidResponseModel, BidStatus, ErrorResponse, Metric, MetricUnit, MetricValue
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection
from placement_controller.jobs.bid_action import BidResponseOrError, ZoneId
from placement_controller.jobs.decision_action import DecisionAction
from placement_controller.jobs.types import ExecutorContext
from placement_controller.membership.types import PlacementZone
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.util.mock_clock import MockClock
from placement_controller.zone.types import ZoneApiFactory


class DecisionActionTest(AsyncTestFixture, ResourceTestFixture):
    clock: MockClock
    name: NamespacedName
    bids: Dict[ZoneId, BidResponseOrError]

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.name = NamespacedName(name="test", namespace="test")

        self.bids = {
            "zone1": BidResponseModel(
                id="1",
                status=BidStatus.accepted,
                reason=None,
                msg=None,
                metrics=[
                    MetricValue(
                        id=Metric.cost,
                        value=Decimal("1.05"),
                        unit=MetricUnit.eur,
                    ),
                ],
            ),
            "zone2": BidResponseModel(
                id="1",
                status=BidStatus.accepted,
                reason=None,
                msg=None,
                metrics=[
                    MetricValue(
                        id=Metric.cost,
                        value=Decimal("1.1"),
                        unit=MetricUnit.eur,
                    ),
                ],
            ),
            "zone3": BidResponseModel(
                id="1", status=BidStatus.rejected, reason="Not enough resources", msg=None, metrics=[]
            ),
            "zone4": ErrorResponse(status=500, code="INTERNAL_ERROR", msg="failure"),
        }

        self.context = ExecutorContext(
            application_controller_client=None,  # type: ignore
            zone_api_factory=ZoneApiFactory(),
            kube_client=FakeClient(),
            clock=self.clock,
        )

    def tearDown(self) -> None:
        super().tearDown()

    def test_decide_success_single_zone_upscale(self) -> None:
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=1,
            current_zones=set(),
            available_zones={"zone1", "zone2", "zone3"},
        )

        action = DecisionAction(self.bids, operation, self.name, "test")
        result = self.loop.run_until_complete(action.run(self.context))

        self.assertEqual(result.result, [PlacementZone(id="zone1")])

    def test_decide_success_multiple_zones_upscale(self) -> None:
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones=set(),
            available_zones={"zone1", "zone2", "zone3"},
        )
        action = DecisionAction(self.bids, operation, self.name, "test")

        result = self.loop.run_until_complete(action.run(self.context))
        self.assertEqual(result.result, [PlacementZone(id="zone1"), PlacementZone(id="zone2")])

    def test_decide_downscale(self) -> None:
        operation = FSMOperation(
            direction=ScaleDirection.DOWNSCALE,
            required_replica=1,
            current_zones={"zone1", "zone2"},
            available_zones={"zone1", "zone2", "zone3"},
        )

        action = DecisionAction(self.bids, operation, self.name, "test")

        result = self.loop.run_until_complete(action.run(self.context))
        self.assertEqual(result.result, [PlacementZone(id="zone1")])
