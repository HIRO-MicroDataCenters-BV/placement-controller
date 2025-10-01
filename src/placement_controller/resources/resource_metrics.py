from typing import Dict, List

from enum import StrEnum

from application_client.models.application_spec import ApplicationSpec
from pydantic_settings import BaseSettings

from placement_controller.api.model import Metric, MetricValue
from placement_controller.resources.types import ResourceMetrics


class EstimateMethod(StrEnum):
    WEIGHTED_AVERAGE = "weighted_average"


class MetricPerUnit(BaseSettings):
    metric: str
    value_per_unit: Dict[str, float]
    method: EstimateMethod


class MetricOptions(BaseSettings):
    static_metrics: List[MetricPerUnit]


class ResourceMetricsImpl(ResourceMetrics):
    config: MetricOptions

    def __init__(self, config: MetricOptions):
        self.config = config

    def estimate(self, spec: ApplicationSpec, metrics: List[Metric]) -> List[MetricValue]:
        estimates: Dict[Metric, float] = {m: 0.0 for m in metrics}
        for resource in spec.resources:
            pass
        results = [MetricValue(id=metric, value=str(value), unit=metric.unit()) for metric, value in estimates.items()]
        return results
