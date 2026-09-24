Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes; surfaces unscored 12; closed-still-broken 0.

Issues filed: 0.

REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1592 — `approve_role_change` rejects `admin_role` that does not match the actor’s assigned role (`tests/python/test_security_model.py::test_role_change_approval_derives_admin_role_from_actor` on tip `82ff0e9`).
REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1593 — same-day distinct destinations get distinct `trip_id` values (`tests/python/test_canonical_trip_plan.py::test_canonical_conversion_generates_distinct_ids_for_distinct_same_day_trips`).
REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1595 — `build_approval_packet` rejects `cost_breakdown` totals that disagree with the trip (`tests/python/test_approval_packet.py::test_build_packet_rejects_cost_breakdown_that_disagrees_with_trip_total`).
REFUTED: https://github.com/stranske/Travel-Plan-Permission/issues/1596 — `check_trip_plan` passes `departure_date` into provider contract evaluation (`tests/python/test_policy_api.py::test_check_trip_plan_uses_departure_date_for_provider_contract`).

## Run report — Track D refill — 2026-09-24

**Repo:** stranske/Travel-Plan-Permission  
**Tip:** `82ff0e9549c55cb10d24fc84b8e60a4b06498295` (+4 commits since 2026-09-23 audit at `3aee8e8`)  
**Unit:** D-audit-Travel-Plan-Permission--2026-09-23T22-11-14Z  
**Executor:** cursor/composer  

### Why this round ran

Fleet refill flagged **no parseable headline** on canonical `Code/Audits/Travel-Plan-Permission/2026-09-23-SCORECARD.md` (template omitted the load-bearing `Scorecard:` line). This run backfills that line and re-scores the product on the current tip after merges for last round’s filings.

### Phase 0–1

- Read dossier, prior OUT (`Travel-Plan-Permission-2026-09-23.md`), repo-audit references, ledger.
- `git pull` on `[LOCAL_WORKSPACE]/Travel-Plan-Permission`: fast-forward to `82ff0e9` (`#1623`–`#1625`, security fix for `#1592`).
- Orientation: **1288** tests collected; **1284** passed locally (1 skipped, 3 xfailed).

### Phase 1.5 (live)

- PP1 varying-input: `check_trip_plan` on minimal canonical plan with `estimated_cost` 500 vs 50000 → **4 vs 5** blocking/error issues (both `status=fail`).
- CLI fill: `fill-spreadsheet` on `tests/fixtures/sample_trip_plan_minimal.json` vs `sample_trip_plan_rich.json` → workbook cell **M7** `2025-10-01` vs `2025-11-12`.
- PP2–PP5, PP7: covered by full pytest green + prior focused portal/exception suites unchanged in intent.
- PP6: still **PARTIAL** (no edit-in-place draft; product contract unchanged).

### Phases 2–4

- Re-ran adversarial checks on modules touched since last audit (`security.py`, `canonical.py`, `approval_packet.py`, `validation.py`, `portal_review.py`, `http_service.py`).
- **#1594** (`trip_plan_from_minimal` / `model_copy` validation bypass) **still reproduces** on tip — e.g. `transportation_mode='spaceship'` is accepted at `src/travel_plan_permission/conversion.py:50`; issue remains open; not re-filed.
- README still documents stale portal URL `/portal/requests/new` at `README.md:119` while the app serves `/portal/draft/new` at `src/travel_plan_permission/http_service.py:1676` — docs debt; deferred (likely overlaps frozen UX issue #1589).
- No new verified, non-duplicate finding met AGENT_ISSUE_FORMAT bar beyond already-tracked open work.

### Delivery

| Item | Status |
|---|---|
| Canonical scorecard | `Code/Audits/Travel-Plan-Permission/2026-09-24-SCORECARD.md` |
| Headline backfill | `2026-09-23-SCORECARD.md` line 3 added |
| AUDIT_LEDGER | updated |
| `gh issue create` | blocked — `gh` not authenticated, no `GH_TOKEN` |
| Intake log | no URL (0 filed) |

**Confidence:** High on scorecard and REFUTED lines (named tests pass on tip). High that **#1594** remains valid (live repro). Medium on whether README staleness is already covered by #1589 (could not query GitHub API). **Would change mind:** a merge that adds `TripPlan.model_validate` after `trip_plan_from_minimal` overrides, or closure of #1594 with a reproduction that no longer applies.
