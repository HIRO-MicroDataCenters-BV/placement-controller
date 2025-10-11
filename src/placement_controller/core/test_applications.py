import asyncio

from application_client import models
from application_client.client import Client
from placement_client import models as placement_client_models

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.core.application import AnyApplication
from placement_controller.core.applications import Applications
from placement_controller.jobs.fake_application_controller import FakeApplicationController
from placement_controller.jobs.fake_placement_server import FakePlacementController
from placement_controller.jobs.types import ExecutorContext
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.settings import PlacementSettings
from placement_controller.util.mock_clock import MockClock
from placement_controller.zone.zone_api_factory import ZoneApiFactoryImpl


class ApplicationsTest(AsyncTestFixture, ResourceTestFixture):
    task: asyncio.Task[None]

    app_server: FakeApplicationController
    zone2_placement_controller: FakePlacementController
    api_factory: ZoneApiFactoryImpl
    app_client: Client

    name: NamespacedName
    client: FakeClient
    clock: MockClock
    settings: PlacementSettings
    executor_context: ExecutorContext

    applications: Applications

    spec: models.ApplicationSpec

    def setUp(self) -> None:
        super().setUp()

        self.app_server = FakeApplicationController(host="127.0.0.1")
        self.app_server.start()

        self.zone2_placement_controller = FakePlacementController(host="127.0.0.1")
        self.zone2_placement_controller.start()

        self.settings = PlacementSettings(
            namespace="test",
            available_zones=["zone1", "zone2"],
            current_zone="zone1",
            application_controller_endpoint=self.app_server.get_base_url(),
            static_controller_endpoints={
                "zone2": self.zone2_placement_controller.get_base_url(),
            },
        )

        self.api_factory = ZoneApiFactoryImpl(self.settings)

        self.app_client = Client(base_url=self.app_server.get_base_url())

        self.clock = MockClock()
        self.client = FakeClient()
        self.name = NamespacedName(name="test", namespace="test")

        self.executor_context = ExecutorContext(
            application_controller_client=self.app_client,
            zone_api_factory=self.api_factory,
            kube_client=self.client,
        )
        self.applications = Applications(self.clock, self.executor_context, self.client, self.terminated, self.settings)
        self.task = self.loop.create_task(self.applications.run())

        self.wait_for_condition(
            2,
            lambda: self.app_server.is_available()
            and self.zone2_placement_controller.is_available()
            and self.applications.is_initialized(),
        )

        self.application = self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", [])
        self.spec = models.ApplicationSpec(
            id=models.ResourceId(name=self.name.name, namespace=self.name.namespace),
            resources=[self.make_pod_spec("pod1", 1, {"cpu": "2", "memory": "200Mi"}, {})],
        )
        self.app_server.mock_response(self.spec)

        self.bid_response = placement_client_models.BidResponseModel(
            id="test",
            status=placement_client_models.BidStatus.ACCEPTED,
            metrics=[
                placement_client_models.MetricValue(
                    id=placement_client_models.Metric.COST, value="1.01", unit=placement_client_models.MetricUnit.EUR
                )
            ],
            reason=None,
            msg="OK",
        )
        self.zone2_placement_controller.mock_response(self.bid_response)

    def tearDown(self) -> None:
        self.task.cancel()
        self.app_server.stop()
        self.zone2_placement_controller.stop()
        super().tearDown()

    def test_ordinary_placement_flow(self) -> None:
        # new application added
        self.loop.run_until_complete(self.client.patch(AnyApplication.GVK, self.application))

        def placements_done() -> bool:
            app_dict = self.loop.run_until_complete(self.client.get(AnyApplication.GVK, self.name))
            if app_dict:
                app = AnyApplication(app_dict)
                return len(app.get_placement_zones()) == 1
            else:
                return False

        self.wait_for_condition(5, placements_done)
