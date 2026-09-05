# Audit run report — Manager-Mosaic (2026-09-05)

**Repo:** [stranske/Manager-Mosaic](https://github.com/stranske/Manager-Mosaic)  
**Base SHA:** `02ffccf` (main, pulled 2026-09-05)  
**Trigger:** Track D refill — agent-ready supply at 2/4 (≤25% threshold)  
**Attempt:** 2 (resumed after missing dossier blocked attempt 1)

## Summary

Attempt 1 stopped because `artifacts/dossiers/Manager-Mosaic.md` was absent. Attempt 2 scoped Phase 0 from README, CLAUDE.md, the 2026-09-04 audit closure note, and R3 synthesis instead.

The repo remains a **young consumer scaffold** (~33 LOC in `src/`), but its charter now defines real product obligations (fact/evidence model, discrepancy detection, thesis monitoring, backplane ingest). The dominant gap class is **charter vs implementation**, not synced CI script defects (those stay upstream in Workflows per the wave-4 correction).

**Filed:** 9 verified AGENT_ISSUE_FORMAT issues (#6–#14). **Retained open:** #3 (core store model, pre-existing).

## Dominant defect classes

1. **Template metadata drift (P2)** — `pyproject.toml` URLs/authors and `Issues.txt` still describe the Template scaffold.
2. **Backplane consumer wiring (P1/P2)** — docs and CI watch for `config/backplane_participants.json` and `tests/fixtures/backplane/`, but neither exists.
3. **Product modules absent (P1)** — evidence validation, numeric discrepancy detection, thesis evaluation, and `fact_key` registry promised in README/R3 but missing from `src/` and `config/`.

## Issues filed

| # | Title | Priority |
|---|---|---|
| [#6](https://github.com/stranske/Manager-Mosaic/issues/6) | pyproject.toml project.urls still reference stranske/Template | P2 |
| [#7](https://github.com/stranske/Manager-Mosaic/issues/7) | pyproject.toml authors remain Template placeholder values | P2 |
| [#8](https://github.com/stranske/Manager-Mosaic/issues/8) | Issues.txt agent queue still documents src/my_project template paths | P2 |
| [#9](https://github.com/stranske/Manager-Mosaic/issues/9) | Add config/backplane_participants.json consumer entry | P1 |
| [#10](https://github.com/stranske/Manager-Mosaic/issues/10) | Add tests/fixtures/backplane evidence-object fixtures | P2 |
| [#11](https://github.com/stranske/Manager-Mosaic/issues/11) | Add manager_mosaic.evidence validate_evidence_object wrapper | P1 |
| [#12](https://github.com/stranske/Manager-Mosaic/issues/12) | Add deterministic numeric discrepancy detection | P1 |
| [#13](https://github.com/stranske/Manager-Mosaic/issues/13) | Add thesis monitoring evaluator with verdict enum | P1 |
| [#14](https://github.com/stranske/Manager-Mosaic/issues/14) | Add config/fact_key_registry.json starter registry | P2 |

## Artifacts

- Run record: `Code/Audits/Manager-Mosaic/2026-09-05-audit-run.md`
- Repo map: `Code/Audits/Manager-Mosaic/2026-09-05-00-repo-map.md`
- Verification log: `Code/Audits/Manager-Mosaic/2026-09-05-verification-log.md`
- Issue bodies: `Code/Audits/Manager-Mosaic/2026-09-05-issue-bodies/`
- Intake log: `~/.codex/orchestrator/measurement/intake-2026-09-04.log` (9 new rows)

## Orientation notes

- Tests collected: 9; local coverage 66.7% (below 80% gate — expected until product modules replace scaffold).
- Synced `scripts/` tree identical to other wave-4 template repos — **not audited for filing** (upstream Workflows).
- Open #3 uses a `## Test Gate` heading instead of `## Acceptance Criteria`; not reformatted in this run — may need a separate format-repair pass if the guard rejects it.

## Confidence

**High** on finding substance — each citation was re-read on tip `02ffccf`. **High** on format compliance — local `issue_format.py` 9/9 pass; remote Agents Issue Format Guard shows **success** on all nine filed titles (#6–#14). **Medium** on fleet-ready dispatch until `agents:formatted` labels land (LMS pattern). **Would change mind** if guard logs later show hard validation failures or `needs-human` labels appear.

## Calibrated dissent

The 2026-09-04 decision to file **zero** issues because the repo was a template skeleton was correct **for synced-script findings**. It is **no longer sufficient** now that README/CLAUDE.md define a product charter and #3 opened the core-model track — the remaining gaps are repo-owned and actionable here, not in Workflows.

Missing dossier is still a process gap; this run proceeded with substitute scope inputs rather than blocking again.
