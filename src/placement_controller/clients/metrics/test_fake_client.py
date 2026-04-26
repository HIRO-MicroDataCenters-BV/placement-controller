from typing import cast

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.metrics.fake_client import FakeMetricsClient


class FakeMetricsClientTest(AsyncTestFixture):
    client: FakeMetricsClient

    def setUp(self) -> None:
        super().setUp()
        self.client = FakeMetricsClient()

    def tearDown(self) -> None:
        super().tearDown()

    def test_increment_counter(self) -> None:
        self.loop.run_until_complete(self.client.increment_counter("test_counter"))
        metric = self.client.get_metric("test_counter")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, str], metric)["type"], "counter")
        self.assertEqual(cast(dict[str, int], metric)["value"], 1)

    def test_increment_counter_with_value(self) -> None:
        self.loop.run_until_complete(self.client.increment_counter("test_counter", value=5))
        metric = self.client.get_metric("test_counter")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, int], metric)["value"], 5)

    def test_increment_counter_with_labels(self) -> None:
        self.loop.run_until_complete(self.client.increment_counter("test_counter", labels={"zone": "zone1"}))
        metric = self.client.get_metric("test_counter", labels={"zone": "zone1"})
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, int], metric)["value"], 1)

    def test_increment_counter_multiple_times(self) -> None:
        self.loop.run_until_complete(self.client.increment_counter("test_counter"))
        self.loop.run_until_complete(self.client.increment_counter("test_counter", value=3))
        metric = self.client.get_metric("test_counter")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, int], metric)["value"], 4)

    def test_set_gauge(self) -> None:
        self.loop.run_until_complete(self.client.set_gauge("test_gauge", 10.5))
        metric = self.client.get_metric("test_gauge")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, str], metric)["type"], "gauge")
        self.assertEqual(cast(dict[str, float], metric)["value"], 10.5)

    def test_set_gauge_with_labels(self) -> None:
        self.loop.run_until_complete(self.client.set_gauge("test_gauge", 20.0, labels={"zone": "zone1"}))
        metric = self.client.get_metric("test_gauge", labels={"zone": "zone1"})
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, float], metric)["value"], 20.0)

    def test_set_gauge_overwrite(self) -> None:
        self.loop.run_until_complete(self.client.set_gauge("test_gauge", 10.0))
        self.loop.run_until_complete(self.client.set_gauge("test_gauge", 20.0))
        metric = self.client.get_metric("test_gauge")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, float], metric)["value"], 20.0)

    def test_observe_histogram(self) -> None:
        self.loop.run_until_complete(self.client.observe_histogram("test_histogram", 1.5))
        self.loop.run_until_complete(self.client.observe_histogram("test_histogram", 2.5))
        metric = self.client.get_metric("test_histogram")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, str], metric)["type"], "histogram")
        self.assertEqual(cast(list[float], metric["values"]), [1.5, 2.5])

    def test_observe_histogram_with_labels(self) -> None:
        self.loop.run_until_complete(self.client.observe_histogram("test_histogram", 1.0, labels={"type": "request"}))
        metric = self.client.get_metric("test_histogram", labels={"type": "request"})
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(list[float], metric["values"]), [1.0])

    def test_record_exception(self) -> None:
        exception = ValueError("Test error")
        self.loop.run_until_complete(self.client.record_exception("test_exception", exception))
        metric = self.client.get_metric("test_exception")
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertEqual(cast(dict[str, str], metric)["type"], "exception")
        self.assertIn("Test error", cast(list[str], metric["exceptions"])[0])

    def test_record_exception_with_labels(self) -> None:
        exception = RuntimeError("Another error")
        self.loop.run_until_complete(
            self.client.record_exception("test_exception", exception, labels={"zone": "zone1"})
        )
        metric = self.client.get_metric("test_exception", labels={"zone": "zone1"})
        self.assertIsNotNone(metric)
        assert metric is not None
        self.assertIn("Another error", cast(list[str], metric["exceptions"])[0])

    def test_get_all_metrics(self) -> None:
        self.loop.run_until_complete(self.client.increment_counter("counter1"))
        self.loop.run_until_complete(self.client.set_gauge("gauge1", 5.0))
        self.loop.run_until_complete(self.client.observe_histogram("hist1", 1.0))
        self.loop.run_until_complete(self.client.record_exception("exc1", ValueError("Test")))

        all_metrics = self.client.get_all_metrics()
        self.assertEqual(len(all_metrics), 4)
        self.assertIn("counter1", all_metrics)
        self.assertIn("gauge1", all_metrics)
        self.assertIn("hist1", all_metrics)
        self.assertIn("exc1", all_metrics)

    def test_metrics_isolated_by_labels(self) -> None:
        self.loop.run_until_complete(self.client.increment_counter("test_counter", labels={"zone": "zone1"}))
        self.loop.run_until_complete(self.client.increment_counter("test_counter", labels={"zone": "zone2"}))

        metric1 = self.client.get_metric("test_counter", labels={"zone": "zone1"})
        metric2 = self.client.get_metric("test_counter", labels={"zone": "zone2"})

        self.assertIsNotNone(metric1)
        self.assertIsNotNone(metric2)
        assert metric1 is not None
        assert metric2 is not None
        self.assertEqual(cast(dict[str, int], metric1)["value"], 1)
        self.assertEqual(cast(dict[str, int], metric2)["value"], 1)

    def test_empty_metric_not_found(self) -> None:
        metric = self.client.get_metric("nonexistent")
        self.assertIsNone(metric)
