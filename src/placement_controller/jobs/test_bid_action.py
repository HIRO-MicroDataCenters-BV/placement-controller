import json
from decimal import Decimal

from application_client.client import Client
from application_client.models import ApplicationSpec, ResourceId
from placement_client import models

from placement_controller.api.model import (
    BidCriteria,
    BidRequestModel,
    BidResponseModel,
    BidStatus,
    Metric,
    MetricUnit,
    MetricValue,
)
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.clients.placement.local import LocalPlacementClient
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection
from placement_controller.jobs.bid_action import BidAction
from placement_controller.jobs.fake_placement_server import FakePlacementController
from placement_controller.jobs.types import ExecutorContext
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.fake_resource_management import FakeResourceManagement
from placement_controller.settings import PlacementSettings
from placement_controller.util.mock_clock import MockClock
from placement_controller.zone.zone_api_factory import ZoneApiFactoryImpl


class BidActionTest(AsyncTestFixture, ResourceTestFixture):

    clock: MockClock
    server1: FakePlacementController
    server2: FakePlacementController
    resource_management: FakeResourceManagement

    name: NamespacedName
    action: BidAction
    spec: ApplicationSpec
    request: BidRequestModel
    response1: models.BidResponseModel
    response2: models.BidResponseModel
    local_bid_response: BidResponseModel

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

        self.clock = MockClock()

        self.name = NamespacedName(name="test", namespace="testns")
        self.spec = ApplicationSpec(
            id=ResourceId(name="test", namespace="test"),
            resources=[self.make_pod_spec("pod1", 1, {"cpu": "2", "memory": "200Mi"}, {})],
        )
        self.request = BidRequestModel(
            id="test", spec=json.dumps(self.spec.to_dict()), bid_criteria=[BidCriteria.cpu], metrics={Metric.cost}
        )
        self.response1 = models.BidResponseModel(
            id="test",
            status=models.BidStatus.ACCEPTED,
            metrics=[models.MetricValue(id=models.Metric.COST, value="1.01", unit=models.MetricUnit.EUR)],
            reason=None,
            msg="OK",
        )
        self.response2 = models.BidResponseModel(
            id="test",
            status=models.BidStatus.ACCEPTED,
            metrics=[models.MetricValue(id=models.Metric.COST, value="1.03", unit=models.MetricUnit.EUR)],
            reason=None,
            msg="OK",
        )
        self.local_bid_response = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.00"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )

        self.server1 = FakePlacementController(host="127.0.0.1")
        self.server1.mock_response(self.response1)
        self.server1.start()

        self.server2 = FakePlacementController(host="127.0.0.1")
        self.server2.mock_response(self.response2)
        self.server2.start()

        self.settings = PlacementSettings(
            namespace="test",
            available_zones=["zone1", "zone2", "zone3"],
            current_zone="zone3",
            application_controller_endpoint="not used",
            static_controller_endpoints={
                "zone1": self.server1.get_base_url(),
                "zone2": self.server2.get_base_url(),
            },
        )
        self.resource_management = FakeResourceManagement()
        self.resource_management.mock_response(self.local_bid_response)

        self.api_factory = ZoneApiFactoryImpl(self.settings, LocalPlacementClient(self.resource_management))
        self.context = ExecutorContext(
            zone_api_factory=self.api_factory,
            application_controller_client=Client(base_url=""),
            kube_client=FakeClient(),
            clock=self.clock,
        )
        self.wait_for_condition(2, lambda: self.server1.is_available() and self.server2.is_available())

    def tearDown(self) -> None:
        super().tearDown()
        self.server1.stop()
        self.server2.stop()

    def test_bid_upscale(self) -> None:
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=1,
            current_zones=set(),
            available_zones={"zone1", "zone2", "zone3"},
        )
        action = BidAction(operation, self.request, self.name)

        result = self.loop.run_until_complete(action.run(self.context))

        self.assertEqual(
            result.response,
            {
                "zone1": BidResponseModel(
                    id="test",
                    status=BidStatus.accepted,
                    reason=None,
                    msg="OK",
                    metrics=[MetricValue(id=Metric.cost, value=Decimal("1.01"), unit=MetricUnit.eur)],
                ),
                "zone2": BidResponseModel(
                    id="test",
                    status=BidStatus.accepted,
                    reason=None,
                    msg="OK",
                    metrics=[MetricValue(id=Metric.cost, value=Decimal("1.03"), unit=MetricUnit.eur)],
                ),
                "zone3": BidResponseModel(
                    id="test",
                    status=BidStatus.accepted,
                    reason=None,
                    msg="OK",
                    metrics=[MetricValue(id=Metric.cost, value=Decimal("1.00"), unit=MetricUnit.eur)],
                ),
            },
        )

    def test_bid_downscale(self) -> None:
        operation = FSMOperation(
            direction=ScaleDirection.DOWNSCALE,
            required_replica=2,
            current_zones={"zone1", "zone2"},
            available_zones={"zone1", "zone2", "zone3"},
        )
        action = BidAction(operation, self.request, self.name)

        result = self.loop.run_until_complete(action.run(self.context))

        self.assertEqual(
            result.response,
            {
                "zone1": BidResponseModel(
                    id="test",
                    status=BidStatus.accepted,
                    reason=None,
                    msg="OK",
                    metrics=[MetricValue(id=Metric.cost, value=Decimal("1.01"), unit=MetricUnit.eur)],
                ),
                "zone2": BidResponseModel(
                    id="test",
                    status=BidStatus.accepted,
                    reason=None,
                    msg="OK",
                    metrics=[MetricValue(id=Metric.cost, value=Decimal("1.03"), unit=MetricUnit.eur)],
                ),
            },
        )
