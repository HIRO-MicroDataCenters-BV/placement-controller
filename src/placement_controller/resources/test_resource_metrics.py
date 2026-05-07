from decimal import Decimal
from time import sleep
from unittest import TestCase

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources
from application_client.models.pod_resources_limits import PodResourcesLimits
from application_client.models.pod_resources_requests import PodResourcesRequests
from application_client.models.pvc_resources import PVCResources
from application_client.models.pvc_resources_limits import PVCResourcesLimits
from application_client.models.pvc_resources_requests import PVCResourcesRequests
from application_client.models.resource_id import ResourceId

from placement_controller.api.model import Metric, MetricUnit, MetricValue
from placement_controller.clients.metrics.fake_client import FakeMetricsClient
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_metrics import (
    DynamicResourceMetrics,
    EstimateMethod,
    MetricDefinition,
    MetricSettings,
    PrometheusMetricDefinition,
    ResourceMetricsImpl,
)


class ResourceMetricsTest(TestCase, ResourceTestFixture):
    def test_dynamic_metrics_combined_static_and_dynamic(self) -> None:
        static_config = MetricSettings(
            static_metrics=[
                MetricDefinition(
                    metric=Metric.cost,
                    value_per_unit={"cpu": Decimal(1.0)},
                    weight={"cpu": Decimal(1.0)},
                    method=EstimateMethod.WEIGHTED_AVERAGE,
                )
            ],
            prometheus_metrics=[
                PrometheusMetricDefinition(
                    metric=Metric.energy,
                    query="node_energy",
                    labels={"zone": "zone1"},
                )
            ],
        )

        fake_client = FakeMetricsClient()
        fake_client.metrics = {"node_energy{zone=zone1}": {"value": 150.5}}

        prometheus_definitions = static_config.prometheus_metrics
        assert prometheus_definitions is not None
        dynamic_metrics = DynamicResourceMetrics(
            static_config=static_config,
            client=fake_client,
            prometheus_definitions=prometheus_definitions,
        )

        pod1 = PodResources(
            id=ResourceId(name="pod1", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1, "memory": 6 * self.GIGA}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[pod1])
        results = dynamic_metrics.estimate(spec, [Metric.cost, Metric.energy])

        cost_result = next(r for r in results if r.id == Metric.cost)
        energy_result = next(r for r in results if r.id == Metric.energy)

        self.assertEqual(cost_result.value, Decimal("1.0000"))
        self.assertEqual(energy_result.value, Decimal("150.5000"))

    def test_dynamic_metrics_fallback_when_prometheus_unavailable(self) -> None:
        static_config = MetricSettings(
            static_metrics=[
                MetricDefinition(
                    metric=Metric.energy,
                    value_per_unit={"cpu": Decimal(0.5)},
                    weight={"cpu": Decimal(1.0)},
                    method=EstimateMethod.WEIGHTED_AVERAGE,
                )
            ],
            prometheus_metrics=[
                PrometheusMetricDefinition(
                    metric=Metric.energy,
                    query="node_energy",
                    labels={"zone": "zone1"},
                )
            ],
        )

        fake_client = FakeMetricsClient()

        prometheus_definitions = static_config.prometheus_metrics
        assert prometheus_definitions is not None
        dynamic_metrics = DynamicResourceMetrics(
            static_config=static_config,
            client=fake_client,
            prometheus_definitions=prometheus_definitions,
        )

        pod1 = PodResources(
            id=ResourceId(name="pod1", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1, "memory": 6 * self.GIGA}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[pod1])
        results = dynamic_metrics.estimate(spec, [Metric.energy])

        energy_result = next(r for r in results if r.id == Metric.energy)

        # Prometheus returns None, no default_value set, so use static estimate (cpu=1, value=0.5 per cpu)
        self.assertEqual(energy_result.value, Decimal("0.5000"))

    def test_dynamic_metrics_missing_static_with_dynamic(self) -> None:
        static_config = MetricSettings(
            static_metrics=[],
            prometheus_metrics=[
                PrometheusMetricDefinition(
                    metric=Metric.energy,
                    query="node_energy",
                    labels={"zone": "zone1"},
                )
            ],
        )

        fake_client = FakeMetricsClient()
        fake_client.metrics = {"node_energy{zone=zone1}": {"value": 200.0}}

        prometheus_definitions = static_config.prometheus_metrics
        assert prometheus_definitions is not None
        dynamic_metrics = DynamicResourceMetrics(
            static_config=static_config,
            client=fake_client,
            prometheus_definitions=prometheus_definitions,
        )

        pod1 = PodResources(
            id=ResourceId(name="pod1", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1, "memory": 6 * self.GIGA}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[pod1])
        results = dynamic_metrics.estimate(spec, [Metric.energy])

        energy_result = next(r for r in results if r.id == Metric.energy)

        self.assertEqual(energy_result.value, Decimal("200.0000"))

    resource_metrics: ResourceMetricsImpl

    pod1: PodResources
    pod2: PodResources
    pod3: PodResources

    def setUp(self) -> None:
        config = MetricSettings(
            static_metrics=[
                MetricDefinition(
                    metric=Metric.cost,
                    value_per_unit={
                        "cpu": Decimal(1.0),
                        "memory": Decimal(0.000000001),
                        "gpu": Decimal(3.0),
                        "storage": Decimal(0.000000001),
                    },
                    weight={
                        "cpu": Decimal(0.25),
                        "memory": Decimal(0.5),
                        "gpu": Decimal(0.5),
                        "storage": Decimal(0.1),
                    },
                    method=EstimateMethod.WEIGHTED_AVERAGE,
                )
            ]
        )
        self.resource_metrics = ResourceMetricsImpl(config)

        self.pod1 = PodResources(
            id=ResourceId(name="pod1", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1, "memory": 6 * self.GIGA}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        self.pod2 = PodResources(
            id=ResourceId(name="pod2", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 3, "gpu": 1}),
            limits=PodResourcesLimits.from_dict({"cpu": 4}),
        )
        self.pod3 = PodResources(
            id=ResourceId(name="pod3", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        self.pvc = PVCResources(
            id=ResourceId(name="pvc1", namespace="test"),
            replica=1,
            storage_class="",
            requests=PVCResourcesRequests.from_dict({"storage": 1 * self.GIGA}),
            limits=PVCResourcesLimits.from_dict({"storage": 2 * self.GIGA}),
        )

    def test_estimate_empty(self):
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[])
        result = self.resource_metrics.estimate(spec, [Metric.cost, Metric.energy])

        self.assertEqual(
            result,
            [
                MetricValue(id=Metric.cost, value=Decimal(0.0000), unit=MetricUnit.eur),
                MetricValue(id=Metric.energy, value=Decimal(0.0000), unit=MetricUnit.watt),
            ],
        )

    def test_estimate_pod(self):
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[self.pod1])
        result = self.resource_metrics.estimate(spec, [Metric.cost, Metric.energy])

        self.assertEqual(
            result,
            [
                MetricValue(id=Metric.cost, value=Decimal("3.4712"), unit=MetricUnit.eur),
                MetricValue(id=Metric.energy, value=Decimal(0), unit=MetricUnit.watt),
            ],
        )

    def test_estimate_pods(self):
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[self.pod1, self.pod2])
        result = self.resource_metrics.estimate(spec, [Metric.cost, Metric.energy])

        self.assertEqual(
            result,
            [
                MetricValue(id=Metric.cost, value=Decimal("5.7212"), unit=MetricUnit.eur),
                MetricValue(id=Metric.energy, value=Decimal(0), unit=MetricUnit.watt),
            ],
        )
