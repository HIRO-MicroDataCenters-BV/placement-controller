from decimal import Decimal
from tempfile import TemporaryDirectory
from unittest import TestCase

from placement_controller.api.model import Metric
from placement_controller.clients.k8s.settings import K8SSettings
from placement_controller.pydantic_yaml import from_yaml, to_yaml
from placement_controller.resources.resource_metrics import EstimateMethod, MetricDefinition, MetricSettings
from placement_controller.settings import ApiSettings, PlacementSettings, PrometheusSettings, Settings


class PyDanticYamlTest(TestCase):
    def test_dump_load_settings(self):
        expected = Settings(
            k8s=K8SSettings(incluster=True, context=None, timeout_seconds=10),
            api=ApiSettings(port=8000),
            placement=PlacementSettings(namespace="test", current_zone="zone1", available_zones=["zone1", "zone2"]),
            prometheus=PrometheusSettings(endpoint_port=8080),
            metrics=MetricSettings(
                static_metrics=[
                    MetricDefinition(
                        metric=Metric.cost,
                        value_per_unit={"cpu": Decimal("1.0")},
                        weight={"cpu": Decimal("0.1")},
                        method=EstimateMethod.WEIGHTED_AVERAGE,
                    )
                ]
            ),
        )
        with TemporaryDirectory("-pydantic", "test") as tmpdir:
            yaml_file = f"{tmpdir}/test.yaml"
            to_yaml(yaml_file, expected)
            actual = from_yaml(yaml_file, Settings)

        self.assertEqual(expected, actual)
