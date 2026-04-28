from typing import Dict

from placement_controller.clients.metrics.types import MetricsClient


class FakeMetricsClient(MetricsClient):
    metrics: Dict[str, Dict[str, float]]

    def __init__(self) -> None:
        self.metrics = {}

    async def get_metric(
        self,
        name: str,
        labels: Dict[str, str] | None = None,
    ) -> Dict[str, float] | None:
        key = self._make_key(name, labels)
        return self.metrics.get(key)

    def get_metric_sync(
        self,
        name: str,
        labels: Dict[str, str] | None = None,
    ) -> Dict[str, float] | None:
        key = self._make_key(name, labels)
        return self.metrics.get(key)

    def _make_key(self, name: str, labels: Dict[str, str] | None) -> str:
        if labels:
            label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            return f"{name}{{{label_str}}}"
        return name
