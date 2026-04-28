# AGENTS.md

A quick start guide for agents working in this repository.

## Navigation

| Document | Purpose |
|----------|---------|
| `ARCHITECTURE.md` | High-level system design and domain structure |
| `DESIGN.md` | Design principles and patterns |
| `PRODUCT_SENSE.md` | Product goals and user needs |
| `QUALITY_SCORE.md` | Quality criteria and testing standards |
| `RELIABILITY.md` | Reliability requirements and SLOs |
| `SECURITY.md` | Security principles and gatekeeping |
| `PLANS.md` | Current and upcoming execution plans |

## Repository Structure

```
docs/
├── design-docs/
│   ├── index.md
│   ├── core-beliefs.md
│   └── ...
├── exec-plans/
│   ├── active/
│   │   └── ...
│   ├── completed/
│   │   └── ...
│   └── tech-debt-tracker.md
├── generated/
│   └── db-schema.md
├── product-specs/
│   ├── index.md
│   ├── new-user-onboarding.md
│   └── ...

```

## Agent Workflow

1. **Start here** - Read `ARCHITECTURE.md` for system overview
2. **Understand goals** - Read `PRODUCT_SENSE.md` for user needs
3. **Check quality** - Review `QUALITY_SCORE.md` for testing standards
4. **Execute** - Follow execution plans in `docs/exec-plans/`
5. **Document** - Add new plans to `docs/exec-plans/active/`

## Core Beliefs

- **Agent-first**: 100% of code is written by agents
- **No manually-written code**: Humans specify intent, agents execute
- **Repository is system of record**: All knowledge is versioned
- **Legibility over style**: Code optimized for agent readability
- **Continuous cleanup**: "Golden principles" enforced mechanically

## Common Tasks

| Task | Where to Start |
|------|----------------|
| Add new feature | `docs/exec-plans/active/` |
| Write tests | `docs/design-docs/` |
| Fix bug | Reproduce via agent, open PR |
| Review PR | Follow agent review flow |
| Update docs | Edit in `docs/` |

## Quick Commands

```bash
# Run tests
uv run pytest

# Type checking
uv run mypy src

# Code formatting
uv run black src

# Linting
uv run flake8 src
```

## Getting Help

- Check `ARCHITECTURE.md` for domain structure
- Review `docs/design-docs/` for implementation details
- Ask for guidance in agent feedback loop

---

*This file is auto-generated. Last updated: 2026-04-27*
