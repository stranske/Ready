# D3 unblock sweep — 2026-10-25T04

**Run:** attempt 1 · sweep time `2026-10-25T04:20:00Z` · **budget 8/15 repos**

**Mode:** synchronous offload — GitHub mutations (issue body/labels, PR labels, fixes) were **not** applied; rows list live state and **recommended** remediations for the driver or next non-offload pass.

**Covered this run:** Workflows, Travel-Plan-Permission, Trend_Model_Project, Portable-Alpha-Extension-Model, Counter_Risk, Manager-Database, Inv-Man-Intake, Pension-Data

**Deferred (next checkpoint):** Ready, trip-planner, learning-management-system, Fine-Art-Archive, Doc-Lineage, Deliverable-Render, Manager-Mosaic · (Orchestrator excluded by policy)

---

## Summary table

| Repo | Frozen (pause / needs-human) | Repaired | Left for owner | Silent claims (>12h, no PR) | Stalled agent PRs (>4h) | Default branch (Gate/CI) | Agent-ready supply |
|------|------------------------------|----------|----------------|-----------------------------|-------------------------|--------------------------|-------------------|
| Workflows | 9 pause · 0 needs-human | 0 | 1 (#3987) | 6 → release† | 0 (add `agent:auto` if >4h) | **RED** Gate `2026-10-16` | 41 |
| Travel-Plan-Permission | 1 pause (#1691) | 0 | 0 | 0 | 0 | Gate success `2026-08-16` (stale) | 5 |
| Trend_Model_Project | 1 pause (#6125) | 0 | 0 | 0 | 0 | No Gate on `main` | 6 |
| Portable-Alpha-Extension-Model | 1 pause (#2430) | 0 | 0 | 0 | 0 | Gate success `2026-08-16` | 21 |
| Counter_Risk | 0 | 0 | 0 | 0 | 0 | No Gate workflow | 2 |
| Manager-Database | 2 pause (#1852, #1773) | 0 | 0 | 1 (#1786) | 0 | Nightly Regression **fail** `2026-10-25` (docker); no Gate | 15 |
| Inv-Man-Intake | 1 pause (#1040) | 0 | 0 | 0 | 0 | No Gate on `main` | 3 |
| Pension-Data | 1 pause (#988) | 0 | 0 | 0‡ | 0 | No Gate; Keepalive Loop Reporter fails (not Gate) | 7 |

† **#4036** still `status:in-progress` with no open PR — recent verifier activity (`2026-10-23`); **do not** blind-release; treat as active investigation unless owner descopes.

‡ **#964** carries `agent:muse` but **open PR #985** cites it — claim must stay until PR closes or issue is descoped.

---

## REFUTATION lines (engine)

REFUTED: https://github.com/stranske/Manager-Database/issues/1773 — named blocker PR #1772 merged 2026-10-16; pause label is stale.

REFUTED: https://github.com/stranske/Workflows/issues/3999 — named delivery PR #3993 merged 2026-10-17; pause label is stale.

---

## Genuinely needs the owner

- **Workflows #3987** — Codex invite policy requires a **human-authored PR** (`compare/main...codex/issue-3987`); automation cannot open the PR. Ask: open the bootstrap PR as author so the lane can proceed (or descope the claim).

---

## Frozen issues — agent-fixable (not applied; offload)

| Issue | Cause (last guard / bot comment) | Recommended fix |
|-------|----------------------------------|-----------------|
| Workflows #4223, #4107, #4051, #3978, #3898 | `format-guard:attempt-cap` (3 optimizer attempts) | Edit body to `docs/AGENT_ISSUE_FORMAT.md`; remove `agents:auto-pilot-pause`. |
| Workflows #4082 | Issue optimizer workflow error | Tighten Tasks/AC with concrete paths under `.github/` / sync manifest; remove pause. |
| Workflows #3901 | `format-guard:attempt-cap` (delivery PR #3902 merged; body still fails guard) | Rewrite Tasks/AC with file paths + runnable test gate; remove pause. |
| Workflows #3999, Manager-Database #1773 | Stale pause after merged delivery | Remove `agents:auto-pilot-pause` only (REFUTED above). |
| Travel #1691, Trend #6125, Portable #2430, Manager #1852, Inv-Man #1040, Pension #988 | `format-guard:attempt-cap` on Python 3.13/3.14 matrix issues — vague task line (“If the 3.14 leg fails…”) | Name concrete files (e.g. `.github/workflows/ci.yml`, matrix keys) and a single verification command; remove pause. |

---

## Silent claims — release `status:in-progress` and `agent:*` (no open PR cites issue)

**Workflows:** #4026, #3988, #3978, #3713 (`agent:retry`). **Also** #3987 after owner PR or explicit descope (currently paused + owner-blocked). **Do not** release #4036 (see †). **#3691** already has `agent:auto` — consider dropping stale `status:in-progress` only if no lane work is expected.

**Manager-Database:** #1786.

**Do not release:** Pension #964 (PR #985 open).

---

## Stalled agent PRs

None met `agent:*` + no update >4h without `agent:auto` already present at sweep time (Workflows #4184/#4139 and Counter_Risk #1185/#1187 updated <1h; Pension #985 ~0.6h, only `agent:muse` — watch for >4h stall → add `agent:auto` per policy).

---

## Red default branch — Workflows

Latest **`Gate` on `main`:** failure `2026-10-16T17:16:30Z` ([run 38938420079](https://github.com/stranske/Workflows/actions/runs/38938420079)).

- **Failure:** `tests/workflows/test_agents_guard_registry_enabled.py::test_shipped_registry_preserves_existing_enabled_routes` — expected enabled routes include `cursor`; actual enabled set is `['claude', 'codex', 'composer', 'cursor', 'gemini', 'muse']` vs expected list with `cursor` but not `muse` (py3.12 and py3.13).
- **Judgment:** registry/shipped-route **fixture drift**, mechanical once current `enabled_routes` policy is confirmed — fix via PR updating test expectation or registry config. **Not attempted** (offload).

**Manager-Database:** latest **Nightly Regression** on `main` failed `2026-10-25` — `dependency api failed to start` in docker compose (infra/transient unless reproducible); not classified as Gate. No `Gate` workflow runs on `main`.

---

## Priority label gap (opener selection)

| Repo | Open issues (≤60 fetched) | With `priority:*` | Implementation issues w/o priority |
|------|---------------------------|-------------------|-------------------------------------|
| Workflows | 57 | 40 | **7:** #4223, #4107, #4087, #3579, #3558, #3557, #3549 (sync-review; first two also paused) |
| Travel-Plan-Permission | 9 | 5 | 0 (5/5 impl issues labelled; 4 trackers lack priority) |
| Trend_Model_Project | 8 | 6 | 0 |
| Portable-Alpha-Extension-Model | 23 | 21 | 0 |
| Counter_Risk | 4 | 2 | 0 |
| Manager-Database | 18 | 15 | **1:** #1773 (paused, no priority) |
| Inv-Man-Intake | 5 | 3 | 0 |
| Pension-Data | 9 | 7 | 0 |

---

## Confidence

- **High:** issue/PR lists, pause counts, silent-claim ages, Workflows Gate failure signature (unchanged since 2026-10-16).
- **Medium:** whether releasing #4036 duplicates verifier work; whether Manager-Database nightly docker failure is flaky vs. defect.
- **Would change mind:** a Gate success on Workflows `main` after `2026-10-16` (none in `gh run list --workflow Gate`); open PRs that reference silent issues only via branch name without `#` in metadata (not seen for listed claims).
