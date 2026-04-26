from typing import Dict

from prometheus_client import REGISTRY, CollectorRegistry, Metric

from placement_controller.clients.metrics.types import MetricsClient


class PrometheusMetricsClient(MetricsClient):
    registry: CollectorRegistry

    def __init__(self, registry: CollectorRegistry | None = None):
        self.registry = registry or REGISTRY

    async def get_metric(
        self,
        name: str,
        labels: Dict[str, str] | None = None,
    ) -> Dict[str, float] | None:
        metrics = self.registry.collect()
        for metric in metrics:
            if metric.name == name:
                return self._extract_metric_value(metric, labels)
        return None

    def _extract_metric_value(self, metric: Metric, labels: Dict[str, str] | None) -> Dict[str, float] | None:
        if labels is None:
            return {"value": self._get_metric_value(metric)}

        for sample in metric.samples:
            if sample.labels == labels:
                return {"value": sample.value}
        return None

    def _get_metric_value(self, metric: Metric) -> float:
        if metric.type == "counter":
            return metric.samples[0].value if metric.samples else 0.0
        elif metric.type == "gauge":
            return metric.samples[0].value if metric.samples else 0.0
        elif metric.type == "histogram":
            count = next((s.value for s in metric.samples if s.name == f"{metric.name}_count"), 0.0)
            return count
        return 0.0
