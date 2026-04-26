from typing import Any

from httpx import AsyncClient

from placement_controller.clients.metrics.types import MetricsClient


class PrometheusMetricsClient(MetricsClient):
    client: AsyncClient
    endpoint: str

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.client = AsyncClient(base_url=endpoint, timeout=30.0)

    async def get_metric(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> dict[str, float] | None:
        query = f"{name}"
        if labels:
            label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
            query = f"{name}{{{label_str}}}"

        response = await self.client.get("/api/v1/query", params={"query": query})
        response.raise_for_status()

        data = response.json()
        result = data.get("data", {}).get("result", [])

        if not result:
            return None

        return {"value": float(result[0].get("value", [None, "0"])[1])}

    async def aclose(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> "PrometheusMetricsClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.aclose()
