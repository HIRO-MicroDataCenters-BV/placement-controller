# Quality Score

Quality criteria and testing standards.

## Testing Requirements

### Unit Tests

| Module Type | Coverage Target |
|-------------|-----------------|
| Core logic (fsm, application) | 95%+ |
| Job actions | 90%+ |
| Resource management | 85%+ |
| Utilities | 80%+ |

### Test Categories

```python
# Category structure
tests/
├── test_fsm_transitions.py      # State machine
├── test_executor_pipeline.py    # Action pipeline
├── test_watcher_changes.py      # Event streams
├── test_resource_placements.py  # Algorithm testing
└── test_integration_lifecycle.py # End-to-end
```

### Test Quality Gates

| Gate | Command | Pass Criteria |
|------|---------|---------------|
| Type Checking | `uv run mypy src` | No errors |
| Linting | `uv run flake8 src` | No violations |
| Formatting | `uv run black --check src` | Clean |
| Tests | `uv run pytest` | 100% pass rate |
| Coverage | `uv run pytest --cov=src` | >85% |

## Code Review Standards

### PR Requirements

- [ ] All tests passing
- [ ] Type checking passes
- [ ] No linter violations
- [ ] Documentation updated
- [ ] Agent reviewers satisfied

### Review Focus

- **Correctness**: Logic verified by tests
- **Legibility**: Agents can understand code
- **Consistency**: Patterns match existing code
- **Completeness**: Edge cases covered

## Performance Thresholds

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| State transition latency | < 100ms | Profiling tests |
| Queue drain time | < 1s | Load tests |
| Memory per application | < 5MB | Metrics |
| API response time | < 100ms | Benchmarks |

## Reliability Requirements

- **99.9% uptime** for scheduling decisions
- **Graceful degradation** on external failures
- **Automatic recovery** from transient errors

---

*Auto-generated from quality standards*
