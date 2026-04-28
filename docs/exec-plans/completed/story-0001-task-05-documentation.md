# Task: Documentation and Config Examples (Story 0001, Task 05)

## Overview

Document the new feature and provide configuration examples.

## Changes

### File: etc/config.yaml

Add prometheus_metrics configuration example:

```yaml
metrics:
  static_metrics:
    - metric: cost
      value_per_unit:
        cpu: 1.0
        memory: 0.000000003
        storage: 0.000000001
        gpu: 3.0
        ephemeral-storage: 0.000000001
      weight:
        cpu: 1.0
        memory: 1.0
        storage: 1.0
        gpu: 1.0
        ephemeral-storage: 1.0
      method: weighted_average
  
  # Optional: Prometheus-based metrics (overrides static values)
  prometheus_metrics:
    - metric: energy
      query: "node_energy_watts"
      labels:
        zone: zone1
      # Optional: default if Prometheus returns no data
      default_value: 0.5
```

### File: docs/exec-plans/active/dynamic-metrics-from-prometheus.md

Update feature description with implementation details.

## Acceptance Criteria

- Configuration example in etc/config.yaml
- Feature description updated with implementation details
- Type checking and tests pass

## Dependencies

All implementation tasks complete
