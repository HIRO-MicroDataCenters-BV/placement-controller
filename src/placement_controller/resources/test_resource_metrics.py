from unittest import TestCase

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources
from application_client.models.pod_resources_limits import PodResourcesLimits
from application_client.models.pod_resources_requests import PodResourcesRequests
from application_client.models.resource_id import ResourceId

from placement_controller.api.model import Metric, MetricUnit, MetricValue
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_metrics import (
    EstimateMethod,
    MetricOptions,
    MetricPerUnit,
    ResourceMetricsImpl,
)


class ResourceMetricsTest(TestCase, ResourceTestFixture):
    resource_metrics: ResourceMetricsImpl

    pod1: PodResources
    pod2: PodResources
    pod3: PodResources

    def setUp(self) -> None:
        options = MetricOptions(
            static_metrics=[
                MetricPerUnit(
                    metric=Metric.cost,
                    value_per_unit={
                        "cpu": 1.0,
                        "memory": 1.0,
                        "memory": 1.0,
                    },
                    method=EstimateMethod.WEIGHTED_AVERAGE,
                )
            ]
        )
        self.resource_metrics = ResourceMetricsImpl(options)

        self.pod1 = PodResources(
            id=ResourceId(name="pod1", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1, "memory": 6 * self.GIGA}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        self.pod2 = PodResources(
            id=ResourceId(name="pod2", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 3}),
            limits=PodResourcesLimits.from_dict({"cpu": 4}),
        )
        self.pod3 = PodResources(
            id=ResourceId(name="pod3", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )

    def test_estimate_empty(self):
        spec = ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[])
        result = self.resource_metrics.estimate(spec, [Metric.cost, Metric.energy])

        self.assertTrue(
            result,
            [
                MetricValue(id=Metric.cost, value="1.0", unit=MetricUnit.eur),
                MetricValue(id=Metric.energy, value="1.0", unit=MetricUnit.watt),
            ],
        )
