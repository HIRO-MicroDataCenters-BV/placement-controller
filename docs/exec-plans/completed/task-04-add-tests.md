# Task: Add Tests for Dynamic Metrics (Story 0001)

## Overview

Add comprehensive tests for dynamic metrics functionality.

## Changes

### File: src/placement_controller/resources/test_resource_metrics.py

Add test class for DynamicResourceMetrics:

```python
class TestDynamicResourceMetrics:
    def _setup(self) -> None:
        self.clock = MockClock()
        self.fake_client = FakeMetricsClient()
    
    def test_combined_static_and_dynamic(self) -> None:
        # Setup: static for cost, dynamic for energy
        static_config = MetricSettings(
            static_metrics=[
                MetricDefinition(
                    metric=Metric.cost,
                    value_per_unit={"cpu": Decimal("1.0")},
                    weight={"cpu": Decimal("1.0")},
                    method=EstimateMethod.WEIGHTED_AVERAGE,
                )
            ],
            prometheus_metrics=[
                PrometheusMetricDefinition(
                    metric=Metric.energy,
                    query="node_energy{zone=\"zone1\"}",
                    labels={"zone": "zone1"},
                )
            ],
        )
        
        dynamic_metrics = DynamicResourceMetrics(
            static_config=static_config,
            client=self.fake_client,
            prometheus_definitions=static_config.prometheus_metrics,
        )
        
        # Setup fake data
        self.fake_client.metrics = {
            "node_energy{zone=zone1}": {"value": 150.5}
        }
        
        # Test: estimate both metrics
        spec = self._create_test_spec()
        results = dynamic_metrics.estimate(spec, [Metric.cost, Metric.energy])
        
        # Verify: cost from static, energy from dynamic
        cost_result = next(r for r in results if r.id == Metric.cost)
        energy_result = next(r for r in results if r.id == Metric.energy)
        
        assert cost_result.value > Decimal(0)
        assert energy_result.value == Decimal("150.5")
    
    def test_fallback_when_prometheus_unavailable(self) -> None:
        # Setup: dynamic metric but no data
        static_config = MetricSettings(
            static_metrics=[
                MetricDefinition(
                    metric=Metric.energy,
                    value_per_unit={"cpu": Decimal("0.5")},
                    weight={"cpu": Decimal("1.0")},
                    method=EstimateMethod.WEIGHTED_AVERAGE,
                )
            ],
            prometheus_metrics=[
                PrometheusMetricDefinition(
                    metric=Metric.energy,
                    query="node_energy{zone=\"zone1\"}",
                    labels={"zone": "zone1"},
                )
            ],
        )
        
        dynamic_metrics = DynamicResourceMetrics(
            static_config=static_config,
            client=self.fake_client,  # Returns None
            prometheus_definitions=static_config.prometheus_metrics,
        )
        
        spec = self._create_test_spec()
        results = dynamic_metrics.estimate(spec, [Metric.energy])
        
        # Verify: falls back to static estimate
        energy_result = next(r for r in results if r.id == Metric.energy)
        assert energy_result.value > Decimal(0)
    
    def test_missing_static_with_dynamic(self) -> None:
        # Setup: only Prometheus metric, no static
        static_config = MetricSettings(
            static_metrics=[],
            prometheus_metrics=[
                PrometheusMetricDefinition(
                    metric=Metric.energy,
                    query="node_energy{zone=\"zone1\"}",
                    labels={"zone": "zone1"},
                )
            ],
        )
        
        dynamic_metrics = DynamicResourceMetrics(
            static_config=static_config,
            client=self.fake_client,
            prometheus_definitions=static_config.prometheus_metrics,
        )
        
        self.fake_client.metrics = {
            "node_energy{zone=zone1}": {"value": 200.0}
        }
        
        spec = self._create_test_spec()
        results = dynamic_metrics.estimate(spec, [Metric.energy])
        
        # Verify: uses dynamic value
        energy_result = next(r for r in results if r.id == Metric.energy)
        assert energy_result.value == Decimal("200.0")
```

## Acceptance Criteria

- Tests for mixed static+dynamic mode
- Tests for fallback when Prometheus unavailable
- Tests for Prometheus-only configuration
- All tests pass
- Coverage > 90% for new code

## Dependencies

Task 1: MetricSettings extended
Task 2: DynamicResourceMetrics implemented
Task 3: Context updated
