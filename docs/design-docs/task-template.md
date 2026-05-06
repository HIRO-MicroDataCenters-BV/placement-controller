# Task Template

Template for structured task tracking in the repository.

## Template

```
## Repository
[repo-name]

## Description
[Brief description of the task]

## Files to Modify
- `path/to/file1.py`—[what to add/modify]
- `path/to/file2.py`—[what to add/modify]

## Implementation Notes
[Key implementation details, patterns to follow]

## Acceptance Criteria
- [ ] [Specific measurable criterion 1]
- [ ] [Specific measurable criterion 2]

## Test Requirements
- [ ] [Test type] in `path/to/tests/` following existing test patterns

## Priority
[critical/high/medium/low]

## Status
[backlog/planned/in-progress/review/completed]
```

## Example

```
## Repository
trustify

## Description
Add a CSV export endpoint for SBOM query results.

## Files to Modify
- `modules/sbom/src/service.rs`—add CSV serialization method
- `modules/sbom/src/endpoints.rs`—add GET handler

## Implementation Notes
Follow the existing JSON export pattern in `SbomService::export_json()`.
Reuse the `QueryResult` type from `modules/sbom/src/model.rs`.

## Acceptance Criteria
- [ ] GET /api/v2/sbom/export?format=csv returns valid CSV
- [ ] Existing JSON export still works

## Test Requirements
- [ ] Integration test in `modules/sbom/tests/` following existing test patterns

## Priority
medium

## Status
planned
```

---

*Auto-generated from task template*
