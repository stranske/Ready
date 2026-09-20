title:	feat: configurable PR health interval via repo variable
state:	MERGED
author:	stranske
labels:	
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
number:	1684
--
## Summary

- Adds a **schedule gate** job to the reusable PR health workflow so consumer repos can control scan frequency via a repository variable — no code changes or PRs required
- Consumer cron runs hourly (`0 * * * *`); the gate checks UTC hour alignment against `PR_HEALTH_INTERVAL_HOURS` and exits early when not aligned (no API calls consumed)
- Manual dispatch (`workflow_dispatch`) always proceeds regardless of interval

### Configuration

Set the repo variable in **Settings → Secrets and variables → Actions → Variables**:

| `PR_HEALTH_INTERVAL_HOURS` | Behavior |
|---|---|
| `1` (default) | Every hour — active development |
| `4` | Every 4 hours |
| `6` | Every 6 hours — moderate activity |
| `12` | Twice daily |
| `0` | Disabled |

### Files changed

| File | Change |
|------|--------|
| `reusable-agents-pr-health.yml` | New `cron_interval_hours` input + gate job; scan and summary gated on it |
| `templates/.../agents-pr-health.yml` | Cron changed to hourly; passes `vars.PR_HEALTH_INTERVAL_HOURS` through |

## Test plan

- [ ] CI passes (actionlint, API wrapper guard, workflow naming)
- [ ] Manual dispatch always runs (gate logs "Manual trigger — always proceeding")
- [ ] Interval=0 skips all work (gate logs "PR Health disabled")
- [ ] Interval=6 only runs at hours 0, 6, 12, 18

🤖 Generated with [Claude Code](https://claude.com/claude-code)
