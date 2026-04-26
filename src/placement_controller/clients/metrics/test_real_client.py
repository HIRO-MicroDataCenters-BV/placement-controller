from prometheus_client import CollectorRegistry, Counter

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.metrics.real_client import PrometheusMetricsClient


class PrometheusMetricsClientTest(AsyncTestFixture):
    client: PrometheusMetricsClient
    registry: CollectorRegistry

    def setUp(self) -> None:
        super().setUp()
        self.registry = CollectorRegistry()
        self.client = PrometheusMetricsClient(registry=self.registry)

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_metric_not_found(self) -> None:
        metric = self.loop.run_until_complete(self.client.get_metric("nonexistent"))
        self.assertIsNone(metric)

    def test_get_metric_not_found_with_labels(self) -> None:
        metric = self.loop.run_until_complete(
            self.client.get_metric("nonexistent", labels={"zone": "zone1"})
        )
        self.assertIsNone(metric)
