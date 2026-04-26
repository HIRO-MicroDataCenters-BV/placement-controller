from typing import Dict


class MetricsClient:
    async def get_metric(
        self,
        name: str,
        labels: Dict[str, str] | None = None,
    ) -> Dict[str, float] | None:
        raise NotImplementedError
