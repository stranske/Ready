## Why

The work-environment response establishes a confirmed capability floor: local Python (non-`PATH` interpreter), Excel/Word via COM, static HTML with working local-file deep links; WebAssembly unverified; **nothing server-hosted or database-backed** ([INFORMATION-REQUEST-RESPONSE.md §A Q1, §A Q3, §F item 17](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md)). Fleet consumer repos receive `templates/consumer-repo/AGENTS.md` and `templates/consumer-repo/config/source_of_truth_docs.yml` via maint-68 sync, but neither file states this environment contract — `AGENTS.md:9-22` covers consumer-repo routing only; `source_of_truth_docs.yml:7-12` lists README and AGENTS focus lines without the work-environment facts. **Missing behavior:** new fleet designs can still assume a hosted service or browser-only delivery because the constraint is not in the template every consumer inherits. **Latent fragility.**

## Scope

Add a fleet-wide **Target work environment** section to the consumer template documenting confirmed capabilities and explicit blocks, synced to all consumers through the existing maint-68 path (`tests/workflows/test_workflow_agents_consolidation.py:136-151` asserts template guard files exist).

## Non-Goals

- Do NOT edit `stranske/Orchestrator`.
- Do NOT change individual product repos' READMEs in this issue — template sync only.
- Do NOT claim WebAssembly/stlite as confirmed — mark it unverified per [response §A Q1 and OWNER_NOTES 2026-09-04 item 2](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md).
- Scaffold-only completion does NOT count: adding a dead link or a one-line note without the quoted hosting block and a contract test is a failure.

## Tasks

- [ ] Add `templates/consumer-repo/docs/TARGET_WORK_ENVIRONMENT.md` with subsections: **Confirmed** (local Python, Office COM, static HTML + local-file deep links), **Unverified** (WebAssembly/Pyodide), **Blocked without redesign** (server-hosted apps, database-backed services) — quoting [response §F item 17](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) for the hosting block.
- [ ] Add a "Target work environment" bullet to `templates/consumer-repo/AGENTS.md` after the Working Stance section (`AGENTS.md:5-8`) pointing agents to `docs/TARGET_WORK_ENVIRONMENT.md` before proposing delivery shapes.
- [ ] Register the new doc in `templates/consumer-repo/config/source_of_truth_docs.yml` with `focus: confirmed work-environment delivery constraints for fleet design`.
- [ ] Register the same path in root `config/source_of_truth_docs.yml` fleet registry (Deliverable-Render entry pattern at lines 163-172).
- [ ] Add `tests/workflows/test_target_work_environment_template.py` asserting the template file exists, contains the quoted hosting sentence, and lists WebAssembly as unverified.
- [ ] Wire the new doc into `.github/sync-manifest.yml` if required for maint-68 delivery (follow existing `AGENTS.md` sync entry pattern).
- [ ] Perform deliberate-break verification (see Acceptance Criteria), capture FAIL output, then revert.

## Acceptance Criteria

- [ ] Named test: `tests/workflows/test_target_work_environment_template.py::test_template_documents_hosting_block` passes — file contains the substring `no server-hosted, database-backed application`.
- [ ] Named test: `tests/workflows/test_target_work_environment_template.py::test_webassembly_marked_unverified` passes.
- [ ] **Deliberate-break gate:** temporarily remove the **Blocked** section from `templates/consumer-repo/docs/TARGET_WORK_ENVIRONMENT.md`. `tests/workflows/test_target_work_environment_template.py::test_template_documents_hosting_block` **must FAIL**. Restore the section after capturing the failure.

## Implementation Notes

- Authoritative source: [INFORMATION-REQUEST-RESPONSE.md](https://github.com/stranske/Ready/blob/main/research-program/artifacts/work-bundle/INFORMATION-REQUEST-RESPONSE.md) §A, §E, §F.
- Confirmed-green local reproduction: `python -m pytest tests/workflows/test_workflow_agents_consolidation.py::test_external_merge_lanes_require_runtime_ac_guard -q` → passes today.
- Consumer template sync path verified at `templates/consumer-repo/` (`README.md:217` in Workflows).
