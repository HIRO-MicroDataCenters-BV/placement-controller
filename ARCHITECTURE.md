# Placement Controller - Architecture

High-level system design and domain structure.

## Overview

The placement-controller implements a distributed placement scheduling system for decentralized control planes.

## Domain Structure

```
placement-controller/
├── core/              # Core scheduling logic
│   ├── fsm.py        # Finite state machine
│   ├── scheduling_queue.py  # Application queue
│   ├── application.py       # Application model
│   ├── context.py           # Execution context
│   └── types.py             # Type definitions
├── jobs/              # Job execution pipeline
│   ├── executor.py     # Agent-based job executor
│   ├── types.py        # Action interfaces
│   └── *.py           # Individual actions
├── resources/         # Resource management
│   ├── node.py        # Node model
│   ├── placement.py   # Placement algorithm
│   └── tracking.py    # Resource tracking
├── membership/        # Zone membership
│   └── watcher.py     # MeshPeer watcher
├── store/             # State persistence
│   └── decision_store.py
├── clients/           # External clients
│   ├── k8s/          # Kubernetes client
│   └── placement/    # Placement client
└── api/               # API endpoints
    └── app.py        # FastAPI application
```

## Domain Layers

Each domain follows a layered architecture:

```
Types → Config → Repo → Service → Runtime → API
```

## External Integrations

- **Kubernetes**: Resource watching and management
- **Placement API**: Cross-zone coordination
- **Prometheus**: Metrics collection
- **FastAPI**: REST endpoints

## Module Dependencies

```
core/ ← jobs/ ← resources/ ← membership/
   ↓                              ↑
   └── clients/ ← store/ ← api/
```

## Key Abstractions

| Abstraction | Purpose |
|-------------|---------|
| `FSM` | State machine for scheduling decisions |
| `Action` | Async task with result handling |
| `SchedulingContext` | Per-application scheduling state |
| `JobExecutor` | Concurrent action execution |

## Error Handling

- Actions retry with exponential backoff
- State timeouts trigger fallback paths
- Graceful degradation on external failures

---

*Auto-generated from codebase structure*
