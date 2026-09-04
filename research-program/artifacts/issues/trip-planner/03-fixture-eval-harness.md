## Why

Need ranking regression harness before live APIs (R7). Verified: `clones/trip-planner/tests/` has `tests/sources/test_adapters.py:10-22` for fixture adapters only — no `tests/eval/` directory. **Missing behavior:** no golden ranking scenarios. **Depends on:** B2-045, B2-046.

## Scope

`tests/eval/test_ranking_fixture.py` loading golden trip scenarios.

## Non-Goals

- Do NOT require live TPP service (B2-051 separate).
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `tests/eval/fixtures/` and `tests/eval/test_ranking_fixture.py`.
- [ ] Document eval command in `docs/contracts/source-adapters.md` companion eval doc.

## Acceptance Criteria

- [ ] Named test: `tests/eval/test_ranking_fixture.py::test_golden_scenario_scores` passes.
- [ ] **Deliberate-break gate:** invert ranking weights → test **must FAIL** → revert.

_Surfaced by B2-047._
