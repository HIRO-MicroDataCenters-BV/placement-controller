from decimal import Decimal

from application_client.client import Client

from placement_controller.api.model import Metric
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.clients.k8s.settings import K8SSettings
from placement_controller.context import Context
from placement_controller.jobs.types import ExecutorContext
from placement_controller.resources.resource_metrics import EstimateMethod, MetricDefinition, MetricSettings
from placement_controller.settings import ApiSettings, PlacementSettings, PrometheusSettings, Settings
from placement_controller.util.clock import Clock
from placement_controller.util.mock_clock import MockClock
from placement_controller.zone.zone_api_factory import ZoneApiFactoryImpl


class ContextTest(AsyncTestFixture):
    clock: Clock
    k8s_client: FakeClient
    executor_context: ExecutorContext
    settings: Settings
    context: Context

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.k8s_client = FakeClient()
        self.app_client = Client(base_url="http://127.0.0.1/")
        self.zone_api_client = ZoneApiFactoryImpl()
        self.executor_context = ExecutorContext(
            application_controller_client=self.app_client, zone_api_factory=self.zone_api_client
        )
        self.settings = self.make_settings()
        self.context = Context(self.clock, self.executor_context, self.k8s_client, self.settings, self.loop)

    def tearDown(self) -> None:
        super().tearDown()

    def test_end_to_end_minimal(self) -> None:
        self.context.start()
        self.wait_for_condition(2, lambda: self.context.resource_tracking.is_subscription_active())
        self.context.stop()

    def make_settings(self) -> Settings:
        settings = Settings(
            k8s=K8SSettings(incluster=True, context=None, timeout_seconds=10),
            api=ApiSettings(port=8000),
            placement=PlacementSettings(namespace="test", current_zone="zone1", available_zones=["zone1", "zone2"]),
            prometheus=PrometheusSettings(endpoint_port=8080),
            metrics=MetricSettings(
                static_metrics=[
                    MetricDefinition(
                        metric=Metric.cost,
                        value_per_unit={"cpu": Decimal(1.0)},
                        weight={"cpu": Decimal(0.25)},
                        method=EstimateMethod.WEIGHTED_AVERAGE,
                    )
                ]
            ),
        )
        return settings
