from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.metrics.fake_client import FakeMetricsClient


class FakeMetricsClientTest(AsyncTestFixture):
    client: FakeMetricsClient

    def setUp(self) -> None:
        super().setUp()
        self.client = FakeMetricsClient()

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
