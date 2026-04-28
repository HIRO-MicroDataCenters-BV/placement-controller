# Task: Extend MetricSettings for Prometheus Metrics (Story 0001)

## Overview

Add support for Prometheus-based metrics configuration alongside existing static metrics.

## Changes

### File: src/placement_controller/resources/resource_metrics.py

#### Modify MetricSettings class

```python
class MetricSettings(BaseSettings):
    static_metrics: List[MetricDefinition]
    prometheus_metrics: Optional[List[PrometheusMetricDefinition]] = None
```

#### Add new PrometheusMetricDefinition class

```python
@dataclass
class PrometheusMetricDefinition:
    metric: Metric
    query: str
    labels: Dict[str, str]
    default_value: Optional[Decimal] = None
```

### File: src/placement_controller/settings.py

No changes required - MetricSettings imported from resource_metrics

### Testing

Update existing tests to test both configurations:
- Static only (existing behavior)
- Mixed static + Prometheus
- Prometheus only

## Acceptance Criteria

- [ ] MetricSettings accepts prometheus_metrics list
- [ ] Backward compatible (existing configs work)
- [ ] Type checking passes

## Dependencies

None - this is infrastructure change
