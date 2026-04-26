class MetricsClient:
    async def increment_counter(
        self,
        name: str,
        value: int = 1,
        labels: dict[str, str] | None = None,
    ) -> None:
        raise NotImplementedError

    async def set_gauge(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        raise NotImplementedError

    async def observe_histogram(
        self,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        raise NotImplementedError

    async def record_exception(
        self,
        name: str,
        exception: Exception,
        labels: dict[str, str] | None = None,
    ) -> None:
        raise NotImplementedError
