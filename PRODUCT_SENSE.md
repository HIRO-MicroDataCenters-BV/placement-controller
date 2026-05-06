# Product Sensing

Product goals and user needs for the placement-controller.

## Target Users

- **Internal SREs**: Monitor and manage multi-zone deployments
- **Developer Platform Teams**: Configure placement strategies
- **Automated Agents**: Execute placement decisions

## Core User Needs

### 1. Reliable Placement

**Need**: Application replicas placed correctly across zones

**Success Metrics**:
- Placement success rate > 99%
- Zone failure recovery < 5 minutes
- Automatic rescheduling on state changes

### 2. Observability

**Need**: Clear visibility into placement decisions

**Success Metrics**:
- All state transitions logged
- Metrics available in Prometheus
- Trace context maintained across zones

### 3. Simplicity

**Need**: Easy to configure and operate

**Success Metrics**:
- Default configuration works out of the box
- Configuration in declarative YAML
- Error messages actionable

## User Journeys

### Journey 1: Deploy New Application

1. Developer creates AnyApplication manifest
2. Agent detects application
3. FSM transitions through states
4. Placements executed across zones
5. Result reported in status

### Journey 2: Handle Zone Failure

1. Zone becomes unavailable
2. Membership watcher detects change
3. FSM detects underprovisioned state
4. Rescheduling triggered
5. Placements updated

### Journey 3: Scale Application

1. Developer updates zones count
2. Agent detects spec change
3. Operation determined (upscale/downscale)
4. New placements scheduled
5. Old placements cleaned up

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to Self-Heal | < 5 min | Zone failure to recovery |

## Constraints

- **Deterministic time**: Testing requires MockClock
- **Repository as system of record**: All knowledge in code

---

*Auto-generated fromproduct requirements*
