from httpx import AsyncClient, Client

from placement_controller.clients.metrics.types import MetricsClient


class PrometheusMetricsClient(MetricsClient):
    endpoint: str

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    async def get_metric(
        self,
        name: str,
        labels: dict[str, str] | None = None,
    ) -> dict[str, float] | None:
        query = f"{name}"
        if labels:
            label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
            query = f"{name}{{{label_str}}}"

        async with AsyncClient(base_url=self.endpoint, timeout=30.0) as client:
            response = await client.get("/api/v1/query", params={"query": query})
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

        with Client(base_url=self.endpoint, timeout=30.0) as client:
            response = client.get("/api/v1/query", params={"query": query})
            response.raise_for_status()

            data = response.json()
            result = data.get("data", {}).get("result", [])

            if not result:
                return None

            return {"value": float(result[0].get("value", [None, "0"])[1])}
