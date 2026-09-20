title:	[P2] Register capability-bundle schema and expand self-smoke validation
state:	CLOSED
author:	stranske
labels:	enhancement, priority:normal
comments:	0
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	560
--
## Why

In scripts/validate_run_contract.py lines 45-51, INGEST_SCHEMA_FILES maps satellite contract schemas for consumer verification, but omits the capability-bundle contract schema mapping despite docs/contracts/schemas/capability-bundle-v1.schema.json existing in the repository. Furthermore, _self_smoke in lines 488-495 validates only three schemas, omitting docs/contracts/schemas/capability-bundle-v1.schema.json and docs/contracts/schemas/tracked-variable-v1.schema.json from Draft202012 schema conformance checks.

## Scope

- Add capability-bundle contract mapping to docs/contracts/schemas/capability-bundle-v1.schema.json in INGEST_SCHEMA_FILES in scripts/validate_run_contract.py.
- Update _self_smoke in scripts/validate_run_contract.py to validate all five schema files under docs/contracts/schemas.
- Add test coverage in tests/test_main.py.

## Non-Goals

- Modifying schema definitions in docs/contracts/schemas.
- Changing run envelope required sections or unsafe raw payload checks.
- Scaffold-only completion does NOT count: adding the schema mapping without expanding _self_smoke coverage is a failure of this issue.

## Tasks

- [ ] Map capability-bundle-v1.schema.json in INGEST_SCHEMA_FILES in scripts/validate_run_contract.py
- [ ] Update _self_smoke in scripts/validate_run_contract.py to check all JSON schema files in docs/contracts/schemas
- [ ] Add unit tests in tests/test_main.py exercising consumer schema validation

## Acceptance Criteria

- `python scripts/validate_run_contract.py --self-smoke --schema-dir docs/contracts/schemas --registry config/backplane_participants.json` passes with all schemas checked.
- `pytest tests/test_main.py` passes with exit code 0.
- Deliberate-break demonstration: removing capability-bundle schema from INGEST_SCHEMA_FILES causes `pytest tests/test_main.py` to fail, and reverting restores pass.

## Implementation Notes

References: Code/Audits/Ready/2026-09-07-00-repo-map.md.
Ensure all schemas remain valid Draft 2020-12 schemas.

