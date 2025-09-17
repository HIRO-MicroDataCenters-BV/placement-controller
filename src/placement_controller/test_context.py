import asyncio
from unittest import TestCase

from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.clients.k8s.settings import K8SSettings
from placement_controller.context import Context
from placement_controller.settings import ApiSettings, PlacementSettings, PrometheusSettings, Settings
from placement_controller.util.clock import Clock
from placement_controller.util.mock_clock import MockClock


class ContextTest(TestCase):
    clock: Clock
    k8s_client: FakeClient

    def setUp(self) -> None:
        self.clock = MockClock()
        self.k8s_client = FakeClient()
        self.settings = self.make_settings()
        self.context = Context(self.clock, self.k8s_client, self.settings, asyncio.get_event_loop())

    def test_end_to_end_minimal(self) -> None:
        self.context.start()

        self.context.stop()

    def make_settings(self) -> Settings:
        settings = Settings(
            k8s=K8SSettings(incluster=True, context=None, timeout_seconds=10),
            api=ApiSettings(port=8000),
            placement=PlacementSettings(namespace="test", current_zone="zone1", available_zones=["zone1", "zone2"]),
            prometheus=PrometheusSettings(endpoint_port=8080),
        )
        return settings
