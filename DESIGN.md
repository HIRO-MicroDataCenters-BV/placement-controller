# Design Principles

Design principles and patterns for the placement-controller.

## Agent-First Development

1. **Legibility Over Style**: Code should be easily understood by agents
2. **Predictable Structure**: Consistent patterns across all modules
3. **Type Safety**: All boundaries are strictly typed
4. **No Secrets**: All configuration in code/repository

## Architectural Patterns

### State Machine Pattern

```python
# Each module has clearly defined states
- UNMANAGED
- PENDING
- FETCH_APPLICATION_SPEC
- BID_COLLECTION
- DECISION
- SET_PLACEMENT
```

### Action Pipeline Pattern

```python
# Async queues for decoupled processing
- incoming: List[Action[T]]
- outgoing: List[ActionResult]
- InProgressAction tracks running tasks
```

### Event Stream Pattern

```python
# Kubernetes-style watchers
- ObjectPool for resource tracking
- Callbacks for state changes
- Declarative reconciliation
```

## Code Organization

### Module Rules

- Each module has one primary responsibility
- Clear separation of concerns
- Dependencies flow "forward" through layers

### Naming Conventions

| Pattern | Example |
|----------|--------|
| Interface | `Clock`, `PlacementClient` |
| Implementation | `MockClock`, `LocalPlacementClient`, `FakeK8sClient` |
| Test Helper | `ResourceTestFixture` |
| Action | `GetSpecAction`, `BidAction` |

## Testing Principles

1. **Deterministic Tests**: Use `MockClock` for time-sensitive code
2. **Isolated unitests**: Every component must be tested in isolation with Fake implementation of external systems as following he Clean Architecture/Hexagonal Arcitecture/Onion Architecture principles. 
3. **Fake and Real API/Client for external systems**: For every external system or service it is required to create a fake client/api that mimics an external system and implements simplified behaviour. Next to fake client/fake api there should be a real production implementation covered by integration tests with external system
4. **Easily runnable tests**: The unitests or integration test should be runnable locally without external system involved by using FakeClients/API.
5. **Isolated State**: Each test creates fresh state
6. **Composability**: Test helpers chain naturally
7. **100% Coverage**: Critical paths require tests

## Async Best Practices

- All async operations use `asyncio`
- No blocking calls in async functions
- Proper cancellation with `is_terminated` event
- Queue drainage verified in tests

## Documentation Standards

- Public methods have docstrings
- Key algorithms documented with state diagrams
- Integration points documented

---

*Auto-generated from design patterns*
