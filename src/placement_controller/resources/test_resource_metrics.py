from decimal import Decimal
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
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_metrics import (
    EstimateMethod,
    MetricDefinition,
    MetricSettings,
    ResourceMetricsImpl,
)


class ResourceMetricsTest(TestCase, ResourceTestFixture):
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
