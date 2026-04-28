# Task: Create DynamicResourceMetrics Wrapper

## Overview

Create a new metrics class that combines static metrics with dynamic Prometheus queries.

## Changes

### File: src/placement_controller/resources/resource_metrics.py

Add new classes for DynamicResourceMetrics that wraps ResourceMetricsImpl and uses Prometheus for dynamic values.

### File: src/placement_controller/clients/metrics/types.py

Add get_metric_sync to MetricsClient interface.

### File: src/placement_controller/clients/metrics/client.py

Add sync implementation for PrometheusMetricsClient.

### File: src/placement_controller/clients/metrics/fake_client.py

Add sync implementation for FakeMetricsClient.

## Acceptance Criteria

- DynamicResourceMetrics implements ResourceMetrics interface
- Combines static + dynamic metrics correctly
- Falls back to static when Prometheus unavailable
- Cache mechanism prevents excessive queries
- All tests pass

## Dependencies

Task 1: MetricSettings extended
