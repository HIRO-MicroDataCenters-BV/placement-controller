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
- Never delete docs without asking permission
- Always update documentation when code changes

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

## Execution Workflow

* Story implementation consists of 3 steps story writing, design writing, and tasks execution

**Story writing**

- Every story must include a task that creates a design doc and an execution plan in `docs/`
- Use story file naming conventions: `story-NNNN-<title>.md`
- See template `docs/design-docs/story-template.md`

**Design writing**

- Design should be detailed enough to allow an agent to break down story into tasks without human intervention
- Use design file naming conventions: `story-NNNN-design-<title>.md`
- See template `docs/design-docs/design-template.md`
- Tasks Break down rules:
   - each task has a scope of one or several units - source file/module/component
   - combination of 1 unit tasks makes an integration task, e.g. file1 + file2 -> module, module1 + module2 -> high level module or component
- Irrespectively of a unit, each self contained change should not break the codebase

**Task Execution** 

- Follow TDD: Write tests first, then implement code to make tests pass
- Every task within a story should complete with all tests passing
- Always pass type checking, linting, and formatting before committing
- Minimize broken code state - each commit should be a working checkpo int

**After execution**

- After each story, update core beliefs with instructions to minimize next human steering
- Always pass type checking, linting, and formatting before committing

---

*Auto-generated from core beliefs*
