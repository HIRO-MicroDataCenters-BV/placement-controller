# Reliability

Reliability requirements and SLOs for the placement-controller.

## Service Level Objectives

| SLO | Target | Measurement Period |
|------|--------|-------------------|
| Placement Success Rate | 99.5% | 30 days |
| State Transition Latency | P95 < 1s | Daily |
| Agent Task Completion | 99% | 30 days |
| No Data Loss | 100% | Per action |

## Error Budget

- **Monthly budget**: 0.5% of placements
- **Alert threshold**: 0.3% (70% of budget)
- **Burn rate calculation**: Actual vs target

## Reliability Patterns

### Retry with Backoff

```python
# Standard retry policy
max_attempts = 3
base_delay = 1s
max_delay = 60s
# Exponential backoff applied
```

### Timeout Management

```python
# Action timeouts
DEFAULT_ACTION_TIMEOUT_SECONDS = 60
DEFAULT_MAX_ACTION_ATTEMPTS = 3
# FSM expires states after timeout
```

### Circuit Breaker

```python
# Failure threshold
failure_threshold = 5
reset_timeout = 30s
# Half-open state before retry
```

## Monitoring & Alerting

### Metrics

- `placement_success_total` (counter)
- `placement_latency_seconds` (histogram)
- `action_retries_total` (counter)
- `state_transitions_total` (counter)

### Alerts

| Alert | Condition | Severity |
|--------|-----------|----------|
| High Failure Rate | > 1% failures in 5m | Critical |
| Slow Transitions | P99 > 5s in 15m | Warning |
| Queue Backlog | > 100 pending actions | Warning |
| Memory Pressure | > 80% usage | Warning |

## Recovery Procedures

### State Machine Recovery

1. Identify stuck state
2. Check action timeout
3. Retry with backoff
4. If exhausted, transition to PENDING

### Resource Cleanup

```bash
# On agent failure
kubectl delete pods -l app=placement-controller
# Restart triggered automatically
```

## Failure Scenarios

### Zone Failure

**Detection**: Membership watcher
**Recovery**: Automatic rescheduling
**RTO**: < 5 minutes

### Agent Crash

**Detection**: Liveness probe
**Recovery**: Pod restart
**RTO**: < 30 seconds

### External API Failure

**Detection**: Error responses
**Recovery**: Retry with backoff
**RTO**: < 60 seconds

---

*Auto-generated from reliability requirements*
