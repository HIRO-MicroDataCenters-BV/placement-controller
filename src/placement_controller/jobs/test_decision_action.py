from typing import Dict

from decimal import Decimal

from placement_controller.api.model import BidResponseModel, BidStatus, ErrorResponse, Metric, MetricUnit, MetricValue
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.core.application import AnyApplication
from placement_controller.jobs.bid_action import BidResponseOrError, ZoneId
from placement_controller.jobs.decision_action import DecisionAction
from placement_controller.jobs.types import ExecutorContext
from placement_controller.membership.types import PlacementZone
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.zone.types import ZoneApiFactory


class DecisionActionTest(AsyncTestFixture, ResourceTestFixture):
    name: NamespacedName
    action: DecisionAction

    app: AnyApplication
    bids: Dict[ZoneId, BidResponseOrError]

    def setUp(self) -> None:
        super().setUp()
        self.name = NamespacedName(name="test", namespace="test")
        dict_app = self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("state", "owner", [])
        self.application = AnyApplication(dict_app)

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
        )
        self.action = DecisionAction(self.bids, self.application, self.name, "test")

    def tearDown(self) -> None:
        super().tearDown()

    def test_decide_success(self) -> None:
        result = self.loop.run_until_complete(self.action.run(self.context))

        self.assertEqual(result.result, [PlacementZone(id="zone1")])
