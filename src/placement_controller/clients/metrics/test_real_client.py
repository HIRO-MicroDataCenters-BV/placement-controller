from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.metrics.real_client import PrometheusMetricsClient


class PrometheusMetricsClientTest(AsyncTestFixture):
    client: PrometheusMetricsClient

    def setUp(self) -> None:
        super().setUp()
        self.client = PrometheusMetricsClient(endpoint="http://localhost:9090")

    def tearDown(self) -> None:
        self.loop.run_until_complete(self.client.aclose())
        super().tearDown()

    def test_init(self) -> None:
        self.assertEqual(self.client.endpoint, "http://localhost:9090")
