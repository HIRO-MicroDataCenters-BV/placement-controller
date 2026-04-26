from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.metrics.client import PrometheusMetricsClient


class PrometheusMetricsClientTest(AsyncTestFixture):
    def test_init(self) -> None:
        client = PrometheusMetricsClient(endpoint="http://localhost:9090")
        self.assertEqual(client.endpoint, "http://localhost:9090")
