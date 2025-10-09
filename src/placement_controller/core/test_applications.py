import asyncio

from application_client.client import Client

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
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

    name: NamespacedName
    client: FakeClient
    clock: MockClock
    settings: PlacementSettings

    def setUp(self) -> None:
        super().setUp()

        self.app_server = FakeApplicationController(host="127.0.0.1")
        self.app_server.start()

        self.zone2_placement_controller = FakePlacementController(host="127.0.0.1")
        self.zone2_placement_controller.start()

        self.api_factory = ZoneApiFactoryImpl()
        self.api_factory.add_static_zone("zone2", self.zone2_placement_controller.get_base_url())

        self.app_client = Client(base_url=self.app_server.get_base_url())

        self.clock = MockClock()
        self.client = FakeClient()
        self.name = NamespacedName(name="test", namespace="testns")
        self.settings = PlacementSettings(namespace="test", available_zones=["zone1", "zone2"], current_zone="zone1")

        self.executor_context = ExecutorContext(
            application_controller_client=self.app_client,
            zone_api_factory=self.api_factory,
            kube_client=self.client,
        )
        self.applications = Applications(self.clock, self.executor_context, self.client, self.terminated, self.settings)
        self.task = self.loop.create_task(self.applications.run())

        self.wait_for_condition(
            2, lambda: self.app_server.is_available() and self.zone2_placement_controller.is_available()
        )

    def tearDown(self) -> None:
        self.app_server.stop()
        self.zone2_placement_controller.stop()
        super().tearDown()
        self.task.cancel()

    def test_ordinary_placement_flow(self) -> None:
        pass
