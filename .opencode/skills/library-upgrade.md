# Skill: Library Upgrade Automation

A structured workflow for upgrading Python libraries and automatically fixing code style/type issues.

## Overview

This skill automates the process of upgrading Python dependencies and fixing resulting code issues using mypy, black, isort, flake8, and pytest.

## Pre-Upgrade Checklist

- [ ] Review `pyproject.toml` or `requirements.txt` for current versions
- [ ] Check for pinned dependencies that may cause conflicts
- [ ] Backup current state (git commit or tag)
- [ ] Review library upgrade notes/changelogs for breaking changes
- [ ] Run current test suite to establish baseline

## Upgrade Steps

### Step 1: Update Dependencies

1. Update version pins in `pyproject.toml` or `requirements.txt`
2. Run dependency resolution:
   ```bash
   uv sync --locked --all-extras --dev  # for uv projects
   # OR
   pip install -r requirements.txt --upgrade  # for pip projects
   ```

### Step 2: Run Static Analysis (mypy)

**Command:**
```bash
uv run mypy ./src
```

**Common Fixes:**

| Error Type | Problem | Solution |
|------------|---------|----------|
| Return type mismatch | Library changed return type | Update annotation to match new return type |
| Parameter type mismatch | Parameter now expects different type | Update parameter type or call site |
| Union type errors | Type narrowing needed | Use `isinstance()` checks or type: ignore |
| Unused imports | Libraries removed imports | Remove unused imports |
| Invalid attribute access | API changed | Use type: ignore[attr-defined] or update code |

### Step 3: Fix Import Order (isort)

**Command:**
```bash
uv run isort ./src
```

**Actions:**
- Imports are organized by category: FUTURE, TYPING, STDLIB, THIRDPARTY, FIRSTPARTY, LOCALFOLDER
- Remove duplicate imports
- Add missing imports if auto-import is enabled

### Step 4: Format Code (black)

**Command:**
```bash
uv run black ./src
uv run black ./src --check --diff  # verify
```

**Actions:**
- Ensure consistent line length
- Format multi-line containers
- Standardize string quotes

### Step 5: Lint Code (flake8)

**Command:**
```bash
uv run flake8 ./src
```

**Common Fixes:**
- Line length violations (E501): Break long lines
- Whitespace issues: Add proper spacing around operators
- Undefined names: Add imports or fix typos
- Unused variables: Remove or prefix with underscore

### Step 6: Run Tests

**Command:**
```bash
uv run pytest
```

**If tests fail:**
1. Read error messages and stack traces
2. Check if test data matches new API
3. Update mocks/stubs to match new signatures
4. Verify imports match library exports

## Common Upgrade Scenarios

### Scenario 1: Breaking API Changes

**Example:**
```python
# Old
def foo(x: str) -> List[str]:
    ...

# New (after upgrade)
def foo(x: str) -> Tuple[str, ...]:
    ...
```

**Fix:**
```python
# Update return type annotation
def foo(x: str) -> Tuple[str, ...]:
    ...
# OR
result = foo(x)
result_list = list(result)  # convert if needed
```

### Scenario 2: Method Signature Changes

**Example:**
```python
# Old
api.list_items(namespace="default", limit=10)

# New
api.list_items(limit=10, namespace="default")  # param order changed
```

**Fix:**
- Update call with correct parameter order
- Use keyword arguments to be safe

### Scenario 3: Type Incompatibility

**Example:**
```python
# Library now expects datetime instead of str
api.create_event(event_time="2024-01-01")  # ERROR
```

**Fix:**
```python
from datetime import datetime, timezone

dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
api.create_event(event_time=dt)
```

### Scenario 4: Dynamic Client API Changes

**Example:**
```python
# Old: DynamicClient methods
async def my_func(client: DynamicClient) -> None:
    api = await client.resources.get(...)

# New: execute() expects DynamicClient | ApiClient
async def my_func(client: DynamicClient | ApiClient) -> None:  # Widen type
    api = await client.resources.get(...)  # ERROR: ApiClient doesn't have .resources
```

**Fix:**
```python
# Option 1: Add type: ignore if safe
async def my_func(client: DynamicClient | ApiClient) -> None:
    api = await client.resources.get(...)  # type: ignore[arg-type]

# Option 2: Use isinstance check
async def my_func(client: DynamicClient | ApiClient) -> None:
    if isinstance(client, DynamicClient):
        api = await client.resources.get(...)
```

### Scenario 5: Custom Objects API

**Example:**
```python
api = CustomObjectsApi(api_client)  # mypy thinks api is CoreV1Api
api.list_namespaced_custom_object(...)  # ERROR
```

**Fix:**
```python
api = CustomObjectsApi(api_client)  # type: ignore
result = api.list_namespaced_custom_object(...)  # type: ignore[attr-defined]
```

## Post-Upgrade Verification

1. **Run full test suite:**
   ```bash
   uv run pytest --cov --cov-report=xml
   ```

2. **Check all quality gates:**
   ```bash
   uv run mypy ./src
   uv run isort ./src --check --diff
   uv run black ./src --check --diff
   uv run flake8 ./src
   ```

3. **Verify changelog:**
   ```bash
   git diff
   git diff --stat
   ```

4. **Commit fixes:**
   ```bash
   git add .
   git commit -m "fix: resolve mypy errors from library upgrades"
   ```

## Troubleshooting

### "No issues found but tests fail"
- Check runtime vs static type errors
- Verify all imports match library exports
- Check for missing type stubs

### "Type ignore comments piling up"
- Consider updating your own type annotations
- Check if library has proper type hints
- Report missing type stubs to library maintainers

### "Tests passing but mypy fails"
- Fix type annotations even if runtime works
- Use `# type: ignore` sparingly and document why

### "Incompatible dependencies"
- Check `uv lock` for conflict messages
- Use `uv pip tree -p` to see dependency tree
- Consider upgrading all packages together

## Quick Reference Commands

```bash
# Full quality check pipeline
uv run mypy ./src && \
uv run isort ./src --check --diff && \
uv run black ./src --check --diff && \
uv run flake8 ./src && \
uv run pytest

# Auto-fix what you can
uv run mypy ./src --install-hooks || true
uv run isort ./src
uv run black ./src
uv run pytest

# Create commit with all changes
git add .
git commit -m "chore: upgrade dependencies and fix code quality"
```

## Notes

- Always commit before major upgrades
- Test in development environment first
- Consider upgrading libraries one at a time for easier debugging
- Check library changelogs for major version upgrades
- Some `# type: ignore` comments may be necessary during transition periods
