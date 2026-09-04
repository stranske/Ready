## Why

Audited financials corpus lane (R6). Verified: `tools/replay/runner.py:1-17` implements golden corpus replay but no N-CSR harvest feeds the corpus (`src/pension_data/harvest/` absent). **Missing behavior:** no N-CSR sample ingest path.

## Scope

Single N-CSR sample ingest path with manifest registration.

## Non-Goals

- Do NOT build full N-CSR bulk downloader.
- Scaffold-only completion does NOT count.

## Tasks

- [ ] Add `src/pension_data/harvest/ncsr_sample.py`.
- [ ] Add `tests/harvest/test_ncsr_sample_offline.py`.

## Acceptance Criteria

- [ ] Named test: `tests/harvest/test_ncsr_sample_offline.py::test_ncsr_fixture_ingests` passes.
- [ ] **Deliberate-break gate:** skip filing date → test **must FAIL** → revert.

_Surfaced by B2-042._
