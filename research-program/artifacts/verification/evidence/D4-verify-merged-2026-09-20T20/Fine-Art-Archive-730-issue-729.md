title:	chore: sync workflow templates
state:	MERGED
author:	stranske
labels:	automated, sync, sync:delivery-ready, workflow:source-sync
comments:	12
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	729
--
## Sync Summary

### Files Updated
- agents-81-gate-followups.yml: Gate followups hub - keepalive and autofix; budgets count Gate failures with failed jobs
- registry.yml: Agent registry - source of truth for agent keys and runner workflow mapping
- agent_registry.js: Agent registry helper - loads registry and resolves agent key from labels
- llm_registry.py: LLM model registry helper - shared slot/model selection and blocked-model enforcement
- MODEL_SELECTION_POLICY.md: Auditable auxiliary-model evaluation, selection, and refresh policy
- model_registry.json: Model registry - available LLM models and their capabilities

---

### Review Checklist
- [ ] CI passes with updated workflows
- [ ] No repo-specific customizations were overwritten

**Source:** stranske/Workflows
**Source SHA:** `11300195bb4e7cf3135d1211a11a850efac10dba`
**Template hash:** `06a120993a95`
**Consumer-sync plan ID:** `sha256:06a120993a957a893fe17371c60d54d88847c55ae27664e8bfd99515e0855596`
**Plan scope:** `source-delta`
**Scope base SHA:** `3ed8bc0a6dbe41d961ba28cf15bf94a54f4679d1`
**Sync phase:** `promote`
**Sync branch:** `sync/workflows-delivery`
**Consumer repo:** `stranske/Fine-Art-Archive`
**Manifest:** `.github/sync-manifest.yml`

<!-- workflow-source:sync_campaign -->
<!-- workflows-consumer-sync:v1 {"schema":"workflows-consumer-sync-pr/v1","consumer_repo":"stranske/Fine-Art-Archive","source_repository":"stranske/Workflows","source_sha":"11300195bb4e7cf3135d1211a11a850efac10dba","template_hash":"06a120993a95","plan_id":"sha256:06a120993a957a893fe17371c60d54d88847c55ae27664e8bfd99515e0855596","plan_scope":"source-delta","scope_base_sha":"3ed8bc0a6dbe41d961ba28cf15bf94a54f4679d1","source_commit":"11300195bb4e7cf3135d1211a11a850efac10dba","sync_phase":"promote","sync_branch":"sync/workflows-delivery","manifest":".github/sync-manifest.yml","lifecycle_state":"staging","run_id":"35486211484","run_attempt":"1","changes_count":6} -->
<!-- sync-pr-delivery-record:v1 {"schema":"sync-pr-delivery-record/v1","durable_issue_url":"https://github.com/stranske/Workflows/issues/1836","plan_id":"sha256:06a120993a957a893fe17371c60d54d88847c55ae27664e8bfd99515e0855596","generation":"06a120993a95","repository":"stranske/Fine-Art-Archive","desired_tree_hash":"495099571ed5f4ee08aeea0bcdfe47fc2e285337","source_commit":"11300195bb4e7cf3135d1211a11a850efac10dba","head_observed_sha":"d818b918a37c56edf57dbab7c2cce5fd278581ef","head_observed_at":"2026-09-20T03:18:55Z","lease_expires_at":"2026-09-23T03:18:56Z","predecessor_prs":[],"successor_prs":[],"delivery_state":"sealed","review_started_at":"2026-09-20T03:29:06.535Z","sealed_at":"2026-09-20T03:46:02.863Z","sealed_head_sha":"d818b918a37c56edf57dbab7c2cce5fd278581ef","review_evidence":{"policy_schema":"workflows.consumer-sync-review-policy/v1","reason":"review_timeout_degraded","degraded":true,"responded_reviewers":[],"unavailable_reviewers":[]},"terminal_disposition":""} -->

autofix: false
