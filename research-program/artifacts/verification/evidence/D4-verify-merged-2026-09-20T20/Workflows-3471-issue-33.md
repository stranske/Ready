title:	chore(codex): bootstrap PR for issue #10
state:	MERGED
author:	stranske
labels:	agent:codex, agents:activated, agents:keepalive, autofix
comments:	5
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	33
--
<!-- pr-preamble:start -->
<!-- pr-preamble:end -->

<!-- auto-status-summary:start -->
## Automated Status Summary
#### Scope
- [ ] Consumers don't know what outputs are available from reusable workflows, making it difficult to chain workflows or use output data. This gap prevents advanced usage patterns.

#### Tasks
- [x] Audit all `workflow_call` outputs in reusable-10-ci-python.yml and other reusable workflows.
- [x] Document each output with name, type, description, and example usage.
- [x] Add examples showing how to use outputs in dependent jobs.
- [x] Create a reference table of all workflow outputs.

#### Acceptance criteria
- [x] - docs/INTEGRATION_GUIDE.md has a "Workflow Outputs" section.
- [x] - All outputs from reusable workflows are documented.
- [x] - At least one example shows chaining workflow outputs to a dependent job.

**Head SHA:** 48ed26e2ab1e06fba03404c5399b75f48cc07819
**Latest Runs:** ⏹️ cancelled — Gate
**Required:** gate: ⏹️ cancelled

| Workflow / Job | Result | Logs |
|----------------|--------|------|
| Agents PR meta manager | ❔ in progress | [View run](https://github.com/stranske/Workflows/actions/runs/20404343827) |
| CI Autofix Loop | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253221) |
| Copilot code review | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253420) |
| Gate | ⏹️ cancelled | [View run](https://github.com/stranske/Workflows/actions/runs/20404253082) |
| Health 40 Sweep | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253206) |
| Health 44 Gate Branch Protection | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253177) |
| Health 45 Agents Guard | ⏹️ cancelled | [View run](https://github.com/stranske/Workflows/actions/runs/20404253049) |
| Health 50 Security Scan | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253183) |
| Maint 52 Validate Workflows | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253192) |
| PR 11 - Minimal invariant CI | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253178) |
| Selftest CI | ✅ success | [View run](https://github.com/stranske/Workflows/actions/runs/20404253189) |
<!-- auto-status-summary:end -->
