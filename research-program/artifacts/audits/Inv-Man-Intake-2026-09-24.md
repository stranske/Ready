Scorecard: 5 work / 2 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 1; closed-still-broken 0.

Issues filed: 0.

REFUTED: https://github.com/stranske/Inv-Man-Intake/issues/693 — `tests/scoring/test_weights_config.py` launch-class cases pass on tip `5f95244`; `compute_score` loads registries via `weights_for_registry()` in `src/inv_man_intake/scoring/engine.py`.

## Run report — Track D refill — 2026-09-24

**Repo:** stranske/Inv-Man-Intake  
**Tip:** `5f95244ae1b7871bc62aee5d86cd3807130224ae` (unchanged since 2026-09-23 rerun)  
**Unit:** D-audit-Inv-Man-Intake--2026-09-24T01-13-11Z  
**Executor:** cursor/composer  

### Why this round ran

The fleet refill table flagged Inv-Man-Intake (1 open agent-ready issue vs last filed set 4) and **`newest_scorecard` could not parse** the canonical `Code/Audits/Inv-Man-Intake/2026-09-23-SCORECARD.md` headline. Root cause: the scorecard template line was omitted under the title (fixed in Dropbox canonical file and in `2026-09-24-SCORECARD.md`).

### Phase 0–1

- Read dossier, prior OUT (`Inv-Man-Intake-2026-09-23.md`), ledger, `docs/PRODUCT_CONTRACT.md`, repo-audit references.
- `git pull` on `[LOCAL_WORKSPACE]/Inv-Man-Intake`: already at tip `5f95244`.
- Orientation: ~17k Python LOC; **1019** tests collected; single CLI `inv-man-ingest`.

### Phase 1.5 (live)

- Staged headless bundles with `tests/fixtures/extraction` bytes (JSON-only layout under `tests/fixtures/intake` is insufficient for raw CLI — matches `tests/conftest.py` / CLI tests).
- Alpha vs Beta variants produced distinct `run_id` values and distinct `identity_refs` fund slugs; both runs emitted full artifact sets including per-field `evidence-*.json` sidecars.
- IMI-5: `final_score` remains `None` with `explainability.status=unavailable` despite available performance — consistent with deliberate production gate at `src/inv_man_intake/v1_smoke.py:399-406` (not filed; prior round withdrew a harmful "fix").
- Focused regression gate: **111 passed** (`cli`, threshold config, weights, validation queue API, evidence emitter, one-pager, report-spec).

### Phases 2–4

No new adversarially verified defect survived dedup against open issues (#948 ontology; #950 report-spec work is already on tip via `src/inv_man_intake/export/report_spec.py` — if that issue remains open, its body is stale, not a new filing) or closed fixes (#693, #966). Dimension scan did not surface interior-only hardening worth filing ahead of the two partial core functions.

### Delivery

| Item | Status |
|---|---|
| Canonical scorecard | `Code/Audits/Inv-Man-Intake/2026-09-24-SCORECARD.md` |
| Headline backfill | `2026-09-23-SCORECARD.md` line 3 added |
| AUDIT_LEDGER | updated |
| `gh issue create` | blocked — `gh` not authenticated, no `GH_TOKEN` |
| Intake log | no URL (0 filed) |

**Confidence:** High that the product scorecard is accurate on this tip (live CLI + 111 tests). Medium on whether #950 remains open (could not query GitHub API from this executor). **Would change mind:** tip advances with a regression in CLI ingest or a merged fix that reopens IMI-5 without evidence-backed components.
