# Core Beliefs

Foundational principles for agent development.

## Agent-First Development

**100% of code is written by agents.** Humans don't write code directly.

- Humans specify *intent*, agents execute *implementation*
- No exceptions for "just this once" manual edits
- Code review happens between agents

## Repository as System of Record

**All knowledge lives in the repository.** Nothing in external tools, docs outside version control, or "tribal knowledge."

- Design docs in `docs/`
- Execution plans in `docs/exec-plans/`
- Architecture in `ARCHITECTURE.md`

## Legibility Over Style

**Code is optimized for agent readability.** Not human aesthetic preferences.

- Clear patterns > clever optimizations
- Self-documenting > dense one-liners
- Consistent structure > variation

## Continuous Cleanup

**"Golden principles" enforced mechanically.** Technical debt paid continuously.

- Agent runs daily to clean up
- Linters enforce rules
- Quality grades track degradation

## Testing Standards

**100% test coverage for critical paths.** No production code without tests.

- Agent generates tests alongside code
- Every python class must have tests
- Coverage gates in CI
- Flaky tests flagged immediately

---

*Auto-generated from core beliefs*
