import asyncio

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.core.applications import Applications
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.settings import PlacementSettings
from placement_controller.util.mock_clock import MockClock


class ApplicationsTest(AsyncTestFixture, ResourceTestFixture):
    task: asyncio.Task[None]

    name: NamespacedName
    client: FakeClient
    clock: MockClock
    settings: PlacementSettings

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.client = FakeClient()
        self.name = NamespacedName(name="test", namespace="testns")
        self.settings = PlacementSettings(namespace="test", available_zones=["zone1", "zone2"], current_zone="zone1")

        self.applications = Applications(self.clock, self.client, self.terminated, self.settings)
        self.task = self.loop.create_task(self.applications.run())

    def tearDown(self) -> None:
        super().tearDown()
        self.task.cancel()

    def test_ordinary_placement_flow(self) -> None:
        pass
