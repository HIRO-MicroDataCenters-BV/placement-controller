from httpx import AsyncClient, Client

from placement_controller.clients.metrics.types import MetricsClient


class PrometheusMetricsClient(MetricsClient):
    async_client: AsyncClient
    sync_client: Client

    def __init__(self, endpoint: str):
        self.async_client = AsyncClient(base_url=endpoint, timeout=30.0)
        self.sync_client = Client(base_url=endpoint, timeout=30.0)

    async def get_metric(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> dict[str, float] | None:
        query = f"{name}"
        if labels:
            label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
            query = f"{name}{{{label_str}}}"

        response = await self.async_client.get("/api/v1/query", params={"query": query})
        response.raise_for_status()

        data = response.json()
        result = data.get("data", {}).get("result", [])
        if not result:
            return None

        return {"value": float(result[0].get("value", [None, "0"])[1])}

    def get_metric_sync(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> dict[str, float] | None:
        query = f"{name}"
        if labels:
            label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
            query = f"{name}{{{label_str}}}"

        response = self.sync_client.get("/api/v1/query", params={"query": query})
        response.raise_for_status()

        data = response.json()
        result = data.get("data", {}).get("result", [])

        if not result:
            return None

        return {"value": float(result[0].get("value", [None, "0"])[1])}
