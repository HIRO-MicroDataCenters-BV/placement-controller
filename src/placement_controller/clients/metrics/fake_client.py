from typing import Any, Dict

from placement_controller.clients.metrics.types import MetricsClient


class FakeMetricsClient(MetricsClient):
    metrics: Dict[str, Dict[str, Any]]

    def __init__(self) -> None:
        self.metrics = {}

    async def increment_counter(
        self,
        name: str,
        value: int = 1,
        labels: Dict[str, str] | None = None,
    ) -> None:
        key = self._make_key(name, labels)
        self.metrics.setdefault(key, {"type": "counter", "value": 0})
        self.metrics[key]["value"] += value

    async def set_gauge(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] | None = None,
    ) -> None:
        key = self._make_key(name, labels)
        self.metrics.setdefault(key, {"type": "gauge", "value": 0.0})
        self.metrics[key]["value"] = value

    async def observe_histogram(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] | None = None,
    ) -> None:
        key = self._make_key(name, labels)
        self.metrics.setdefault(key, {"type": "histogram", "values": []})
        self.metrics[key]["values"].append(value)

    async def record_exception(
        self,
        name: str,
        exception: Exception,
        labels: Dict[str, str] | None = None,
    ) -> None:
        key = self._make_key(name, labels)
        self.metrics.setdefault(key, {"type": "exception", "exceptions": []})
        self.metrics[key]["exceptions"].append(str(exception))

    def _make_key(self, name: str, labels: Dict[str, str] | None) -> str:
        if labels:
            label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            return f"{name}{{{label_str}}}"
        return name

    def get_metric(self, name: str, labels: Dict[str, str] | None = None) -> Dict[str, Any] | None:
        key = self._make_key(name, labels)
        return self.metrics.get(key)

    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        return dict(self.metrics)
