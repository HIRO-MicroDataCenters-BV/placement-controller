from typing import Dict, List, Optional, Set

import asyncio
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from time import time

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources
from application_client.models.pvc_resources import PVCResources
from kubernetes.utils.quantity import parse_quantity
from loguru import logger
from pydantic import field_validator
from pydantic_settings import BaseSettings

from placement_controller.api.model import Metric, MetricValue
from placement_controller.clients.metrics.types import MetricsClient
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

    @field_validator("value_per_unit", "weight", mode="before")
    def convert_decimal(cls, v):
        return {k: Decimal(str(val)) for k, val in v.items()}


@dataclass
class PrometheusMetricDefinition:
    metric: Metric
    query: str
    labels: Dict[str, str]
    default_value: Optional[Decimal] = None


class MetricSettings(BaseSettings):
    static_metrics: List[MetricDefinition]
    prometheus_metrics: Optional[List[PrometheusMetricDefinition]] = None


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


@dataclass
class CachedMetricValue:
    value: MetricValue
    query_time: float


class DynamicResourceMetrics(ResourceMetrics):
    static_metrics: ResourceMetricsImpl
    client: MetricsClient
    prometheus_definitions: List[PrometheusMetricDefinition]
    cache: Dict[str, CachedMetricValue]
    cache_ttl_seconds: int = 60
    last_update: Optional[float] = None
    prometheus_update_interval: float = 1.0
    is_terminated: asyncio.Event

    def __init__(
        self,
        static_config: MetricSettings,
        client: MetricsClient,
        prometheus_definitions: List[PrometheusMetricDefinition],
        is_terminated: asyncio.Event,
        prometheus_update_interval: float = 1.0,
    ):
        self.static_metrics = ResourceMetricsImpl(config=static_config)
        self.client = client
        self.prometheus_definitions = prometheus_definitions
        self.cache = {}
        self.prometheus_update_interval = prometheus_update_interval
        self.is_terminated = is_terminated

    def estimate(self, spec: ApplicationSpec, metrics: List[Metric]) -> List[MetricValue]:
        static_estimates = self.static_metrics.estimate(spec, metrics)

        self._update_prometheus_metrics()

        results = []
        for metric in metrics:
            if metric in self.cache:
                cache_entry = self.cache[metric]
                if self._is_cache_valid(cache_entry):
                    results.append(cache_entry.value)
                else:
                    static_value = next((v for v in static_estimates if v.id == metric), None)
                    if static_value:
                        results.append(static_value)
                    else:
                        results.append(MetricValue(id=metric, value=Decimal(0), unit=metric.unit()))
            else:
                static_value = next((v for v in static_estimates if v.id == metric), None)
                if static_value:
                    results.append(static_value)
                else:
                    results.append(MetricValue(id=metric, value=Decimal(0), unit=metric.unit()))

        return results

    def _should_update_prometheus(self) -> bool:
        if self.last_update is None:
            return True
        return time() - self.last_update >= self.prometheus_update_interval

    def _update_prometheus_metrics(self) -> None:
        if not self._should_update_prometheus():
            return
        current_time = time()
        for prom_def in self.prometheus_definitions:
            result = self.client.get_metric_sync(prom_def.query, prom_def.labels)
            if result and "value" in result:
                value = Decimal(str(result["value"]))
                metric_value = MetricValue(
                    id=prom_def.metric, value=value.quantize(Decimal("1.0001")), unit=prom_def.metric.unit()
                )
                self.cache[prom_def.metric] = CachedMetricValue(value=metric_value, query_time=current_time)
            elif prom_def.default_value is not None:
                metric_value = MetricValue(
                    id=prom_def.metric,
                    value=prom_def.default_value.quantize(Decimal("1.0001")),
                    unit=prom_def.metric.unit(),
                )
                self.cache[prom_def.metric] = CachedMetricValue(value=metric_value, query_time=current_time)
        self.last_update = current_time

    def _is_cache_valid(self, entry: CachedMetricValue) -> bool:
        if self.cache_ttl_seconds <= 0:
            return True
        return time() - entry.query_time < self.cache_ttl_seconds

    async def prometheus_update_loop(self) -> None:
        while not self.is_terminated.is_set():
            try:
                await asyncio.sleep(self.prometheus_update_interval)
                current_time = time()
                for prom_def in self.prometheus_definitions:
                    result = await self.client.get_metric(prom_def.query, prom_def.labels)
                    if result and "value" in result:
                        value = Decimal(str(result["value"]))
                        metric_value = MetricValue(
                            id=prom_def.metric, value=value.quantize(Decimal("1.0001")), unit=prom_def.metric.unit()
                        )
                        self.cache[prom_def.metric] = CachedMetricValue(value=metric_value, query_time=current_time)
                    elif prom_def.default_value is not None:
                        metric_value = MetricValue(
                            id=prom_def.metric,
                            value=prom_def.default_value.quantize(Decimal("1.0001")),
                            unit=prom_def.metric.unit(),
                        )
                        self.cache[prom_def.metric] = CachedMetricValue(value=metric_value, query_time=current_time)
            except asyncio.CancelledError:
                logger.error("_prometheus_update_loop is cancelled")
                break
            except Exception as e:
                logger.error(f"Error in _prometheus_update_loop: {e}")
