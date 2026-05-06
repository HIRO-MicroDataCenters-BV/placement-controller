# Dynamic Metrics from Prometheus

## Overview

Enable the placement-controller to load cost and energy metrics from Prometheus in addition to the existing static configuration. This provides real-time metrics while maintaining backward compatibility with static configuration.

## Problem Statement

Currently, cost and energy metrics are statically configured in `config.yaml`. This approach has limitations:
- Metrics are fixed at startup, no real-time updates
- Cannot adapt to changing pricing/energy data without restart
- No integration with existing Prometheus monitoring infrastructure

## Solution

Implement a hybrid metrics system that:
1. Maintains static configuration (backward compatible)
2. Loads metrics from Prometheus via the existing client
3. Supports mixed mode: static defaults + dynamic overrides

## Design

### Architecture

```
MetricSettings
├── static_metrics (existing)
└── prometheus_metrics (new)
    ├── metric_name
    ├── query_template
    └── labels

ResourceMetricsImpl (static) + PrometheusMetricsClient (dynamic)
                    ↓
           DynamicResourceMetrics (wrapper)
                    ↓
              Combined estimates
```

### Configuration

```yaml
metrics:
  static_metrics:
    - metric: cost
      value_per_unit:
        cpu: 1.0
      weight:
        cpu: 1.0
      method: weighted_average
  
  prometheus_metrics:
    - metric: energy
      query: "node_energy_watts"
      labels:
        zone: zone1
```

### Behavior

- Static metrics always loaded first
- Prometheus metrics queried for dynamic values
- Missing Prometheus data falls back to static values
- Failed queries logged but don't break scheduling

## Execution Instructions

**Execute using TDD principle with minimal broken code.** After each module and task:
- Write tests first, then implement code
- Every commit should be a working checkpoint with all tests passing
- Follow existing code patterns (e.g., `test_resource_metrics.py` for test structure)
- Run `uv run pytest`, `uv run mypy src`, `uv run black src`, and `uv run flake8 src` before committing

## Tasks Completed

1. ✅ Story 0001, Task 01: Extend MetricSettings for Prometheus Metrics
2. ✅ Story 0001, Task 02: Create DynamicResourceMetrics wrapper class
3. ✅ Story 0001, Task 03: Update Context to initialize Prometheus client
4. ✅ Story 0001, Task 04: Add tests for DynamicResourceMetrics
5. ✅ Story 0001, Task 05: Documentation and config examples

## Success Criteria

- ✅ Metrics can be loaded from Prometheus
- ✅ Static metrics still work (backward compatible)
- ✅ Fallback to static when Prometheus unavailable
- ✅ All existing tests pass
- ✅ New tests cover dynamic metrics paths
