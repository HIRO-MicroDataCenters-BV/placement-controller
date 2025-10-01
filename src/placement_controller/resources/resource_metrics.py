from typing import Dict, List, Set

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources
from application_client.models.pvc_resources import PVCResources
from kubernetes.utils.quantity import parse_quantity
from pydantic_settings import BaseSettings

from placement_controller.api.model import Metric, MetricValue
from placement_controller.resources.types import ResourceMetrics

ResourceName = str
CostPerUnit = Decimal
ResourceWeight = Decimal


class EstimateMethod(StrEnum):
    WEIGHTED_AVERAGE = "weighted_average"


class MetricDefinition(BaseSettings):
    metric: Metric
    value_per_unit: Dict[str, Decimal]
    weight: Dict[str, Decimal]
    method: EstimateMethod


class MetricSettings(BaseSettings):
    static_metrics: List[MetricDefinition]


class ResourceMetricsImpl(ResourceMetrics):
    config: MetricSettings

    def __init__(self, config: MetricSettings):
        self.config = config

    def estimate(self, spec: ApplicationSpec, metrics: List[Metric]) -> List[MetricValue]:
        estimates: Dict[Metric, Decimal] = {m: Decimal(0.0) for m in metrics}
        for resource in spec.resources:
            if isinstance(resource, PodResources):
                requests = {
                    resource_name: parse_quantity(resource.requests[resource_name])
                    for resource_name in resource.requests.additional_keys
                }
                limits = {
                    resource_name: parse_quantity(resource.limits[resource_name])
                    for resource_name in resource.limits.additional_keys
                }

                self.estimate_metric(estimates, requests, limits, resource.replica)
            elif isinstance(resource, PVCResources):
                requests = {
                    resource_name: parse_quantity(resource.requests[resource_name])
                    for resource_name in resource.requests.additional_keys
                }
                limits = {
                    resource_name: parse_quantity(resource.limits[resource_name])
                    for resource_name in resource.limits.additional_keys
                }

                self.estimate_metric(estimates, requests, limits, resource.replica)
            else:
                raise Exception(f"Unsupported resource type {type(resource)}")

        results = [
            MetricValue(id=metric, value=value.quantize(Decimal("1.0001")), unit=metric.unit())
            for metric, value in estimates.items()
        ]
        return results

    def estimate_metric(
        self,
        estimates_out: Dict[Metric, Decimal],
        requests: Dict[ResourceName, Decimal],
        limits: Dict[ResourceName, Decimal],
        replica: int,
    ) -> None:

        for metric_per_unit in self.config.static_metrics:
            estimation_method = WeightedAverage(
                weights=metric_per_unit.weight, cost_per_unit=metric_per_unit.value_per_unit
            )
            estimate = estimation_method.estimate(requests, limits)

            total = estimates_out.get(metric_per_unit.metric, Decimal(0))
            total += estimate * replica
            estimates_out[metric_per_unit.metric] = total


@dataclass
class WeightedAverage:
    weights: Dict[ResourceName, ResourceWeight]
    cost_per_unit: Dict[ResourceName, CostPerUnit]

    def estimate(self, requests: Dict[ResourceName, Decimal], limits: Dict[ResourceName, Decimal]) -> Decimal:
        resources: Set[ResourceName] = set(requests.keys()) | set(limits.keys())
        result = Decimal(0.0)
        for resource_name in resources:
            resource_units = Decimal(requests.get(resource_name, limits.get(resource_name, Decimal(0.0))))
            cost_per_unit = self.cost_per_unit.get(resource_name) or Decimal(0.0)
            resource_weight = self.weights.get(resource_name) or Decimal(0.0)
            result = result + resource_units * cost_per_unit * resource_weight
        return result
