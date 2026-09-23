Scorecard: 6 work / 1 partial / 0 broken / 0 fabricated / 0 not exercised of 7; journey: passes (policy verdict varies with inputs; portal/manager/exception paths green in suite; PP6 still partial—corrections require new draft); surfaces unscored 12; closed-still-broken 0.

Issues filed: 5 — [#1592](https://github.com/stranske/Travel-Plan-Permission/issues/1592), [#1593](https://github.com/stranske/Travel-Plan-Permission/issues/1593), [#1594](https://github.com/stranske/Travel-Plan-Permission/issues/1594), [#1595](https://github.com/stranske/Travel-Plan-Permission/issues/1595), [#1596](https://github.com/stranske/Travel-Plan-Permission/issues/1596). Format guard: `agents:formatted` on all five (Agents Issue Intake success on sampled runs).

## Run report

**Unit:** `D-audit-Travel-Plan-Permission--2026-09-23T09-11-15Z`  
**Tip:** `3aee8e887ec81a54ce2aa2d75fd82017a952d7c1` (`main`, shallow clone pulled at start)  
**Method:** repo-audit Phase 0 (dossier + ledger), Phase 1 orientation (1275 tests collect, 1271 pass), Phase 1.5 scorecard (contract PP1–PP7 + CLI fill), Phases 2–3 focused D1/D3 (security, canonical IDs, conversion, approval packet, policy_api wiring), adversarial verification on live tip, dedup against open issues (#1570 terminal replay is separate from #1592).

### Scorecard notes

- **PP1:** `check_trip_plan` with estimated_cost 500 vs 50000 → both `fail`, issue count 5 vs 6.
- **PP4:** exercised via `test_http_service` exception/escalation tests (55 selected passed); upgrades tier after 48h.
- **CLI fill:** `fill-spreadsheet` on `sample_trip_plan_minimal.json` vs `sample_trip_plan_rich.json` → departure cell M7 differs.
- **PP6:** still **PARTIAL** (no edit-in-place draft; product contract unchanged).

### Findings filed (verified)

| Issue | Summary |
|---|---|
| #1592 | `SecurityModel` role-change approval trusts `admin_role` parameter, not actor assignment |
| #1593 | Canonical `_default_trip_id` collides for same traveler/day |
| #1594 | `trip_plan_from_minimal` `model_copy` skips validation on overrides |
| #1595 | `build_approval_packet` honors mismatched `cost_breakdown` totals |
| #1596 | `check_trip_plan` omits `plan.departure_date` for `validate_plan` / provider contracts |

### Deferred (evidence retained, not filed)

- SQLite `load_snapshot` without read lock during `replace=True` save (`sqlite_store.py:98-106`) — overlaps partially with closed #1432 write concurrency; needs isolated repro test before filing.
- Postgres `_select_all` unconditional `commit()` (`postgres_store.py:97`) — same class; no open duplicate found; deferred to avoid stacking with unresolved #1432 follow-through.
- README still documents `/portal/requests/new` (`README.md:110`) while app serves `/portal/draft/new` — docs-only; lower priority than open #1589 UX.

### Continuity artifacts

- `Code/Audits/Travel-Plan-Permission/2026-09-23-SCORECARD.md`
- `Code/Audits/Travel-Plan-Permission/2026-09-23-audit-run.md`
- Issue bodies: `artifacts/audits/Travel-Plan-Permission-2026-09-23-issue-bodies/01..05`
- Intake log rows appended for #1592–#1596

### CI / environment

- Local pytest green; no in-browser portal drive (TestClient + CLI/API per scorecard rules).
- `gh issue create` required `export GH_TOKEN=$(gh auth token)` in this seat.
