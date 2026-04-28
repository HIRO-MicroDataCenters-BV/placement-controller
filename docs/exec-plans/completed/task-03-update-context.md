# Task: Update Context to Initialize Dynamic Metrics (Story 0001)

## Overview

Modify context.py to inject Prometheus client and initialize dynamic metrics.

## Changes

### File: src/placement_controller/context.py

Import PrometheusMetricsClient and MetricsClient:

```python
from placement_controller.clients.metrics.client import PrometheusMetricsClient
from placement_controller.clients.metrics.types import MetricsClient
```

Modify Context class to initialize dynamic metrics when prometheus_metrics configured:

```python
class Context:
    settings: Settings
    metrics_client: Optional[MetricsClient]
    resource_metrics: ResourceMetricsImpl

    def __init__(
        self,
        clock: Clock,
        app_client: Client,
        decision_store: DecisionStore,
        zone_api_factory: ZoneApiFactoryImpl,
        kube_client: KubeClient,
        settings: Settings,
        loop: asyncio.AbstractEventLoop,
    ):
        self.settings = settings
        self.terminated = asyncio.Event()
        self.loop = loop
        self.tasks = []
        
        # Initialize Prometheus client if configured
        self.metrics_client: Optional[MetricsClient] = None
        if self.settings.metrics.prometheus_metrics:
            from placement_controller.clients.metrics.client import PrometheusMetricsClient
            self.metrics_client = PrometheusMetricsClient(
                endpoint=self.settings.prometheus_client.endpoint
            )
        
        # Initialize resource metrics
        self._init_resource_metrics()

    def _init_resource_metrics(self) -> None:
        from placement_controller.resources.resource_metrics import DynamicResourceMetrics
        
        if self.settings.metrics.prometheus_metrics:
            self.resource_metrics = DynamicResourceMetrics(
                static_config=self.settings.metrics,
                client=self.metrics_client,
                prometheus_definitions=self.settings.metrics.prometheus_metrics,
            )
        else:
            self.resource_metrics = ResourceMetricsImpl(config=self.settings.metrics)
```

## Acceptance Criteria

- Prometheus client initialized when config has prometheus_metrics
- Static-only mode works (backward compatible)
- Context can be instantiated with either configuration
- All tests pass

## Dependencies

Task 1: MetricSettings extended
Task 2: DynamicResourceMetrics implemented
