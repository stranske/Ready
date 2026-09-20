title:	Create integration test consumer repository
state:	CLOSED
author:	github-actions
labels:	agent:codex, enhancement, status:in-progress, testing
comments:	4
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	17
--
Topic GUID: 24be3dee-d72e-519e-927f-8b25052b55f9

## Why
Currently there's no real-world validation that the reusable workflows work correctly for external consumers. An integration test repo would catch issues before they affect real users.
Scope
- New repository `stranske/Workflows-integration-test` that consumes this workflow library.

## Tasks
- [ ] Create minimal Python project repository.
- [ ] Configure CI using reusable workflows from stranske/Workflows.
- [ ] Add workflow that runs on schedule and on workflow library releases.
- [ ] Test multiple configurations: basic, full coverage, monorepo simulation.
- [ ] Report integration test status back to main repo via badge or notification.

## Acceptance criteria
- Integration test repo exists and runs CI successfully.
- Tests exercise reusable-10-ci-python.yml with various input combinations.
- Failures in integration tests create issues in stranske/Workflows.
- Badge in README.md shows integration test status.

## Implementation notes
- Use `workflow_dispatch` with `repository_dispatch` to trigger on releases.
- Include edge cases: no pyproject.toml, minimal project, coverage disabled.
- Consider testing `@main`, `@v1`, and specific version tags.

---
Synced by [workflow run](https://github.com/stranske/Workflows/actions/runs/20392702689).
