## Why (verified evidence)

`detect_numeric_discrepancies()` groups competing facts only when `(fact_key, entity_ref, period)` match with **exact string equality** on `period` (`src/manager_mosaic/discrepancy.py:70-72`). The fleet mosaic-core contract requires joins on `(fact_key, entity_ref, period)` **after explicit period normalization** (`docs/contracts/mosaic-core-v1.md:59-60`). The thesis evaluator already normalizes quarter labels via `_period_chronology_key()` (`src/manager_mosaic/thesis.py:25-32`), but discrepancy detection does not, so the same quarter spelled two ways never competes.

On tip `e0fe240`, `detect_numeric_discrepancies()` returns **no** discrepancy for `2024Q4` at 12.0 vs `Q4 2024` at 18.0 (50% spread), while identical values under a single label flag correctly. A user comparing manager sources with mixed period spellings can miss a material numeric conflict.

## Tasks

- [ ] Add a shared period chronology helper (extract from `src/manager_mosaic/thesis.py:25-32` or equivalent) usable by both thesis and discrepancy modules without circular imports.
- [ ] In `src/manager_mosaic/discrepancy.py:70-72`, group facts by `(fact_key, entity_ref, normalized_period_key)` where `normalized_period_key` comes from the shared helper; preserve a stable representative `period` string on `DiscrepancyRecord` (document the choice in code).
- [ ] In `tests/test_discrepancy_detection.py`, add `test_detect_numeric_discrepancies_groups_equivalent_period_labels` asserting `2024Q4` vs `Q4 2024` conflicting IRR values produce one `numeric_delta` discrepancy.

## Acceptance Criteria

- Named test: `tests/test_discrepancy_detection.py::test_detect_numeric_discrepancies_groups_equivalent_period_labels` asserts one discrepancy for alias period labels with conflicting values above threshold.
- Deliberate-break → revert: at `src/manager_mosaic/discrepancy.py:70-72`, temporarily group on raw `fact.period` instead of the normalized key → confirm the named test **FAILS** → restore normalized grouping → named test passes.
- `python3 -m pytest -q --no-cov tests/test_discrepancy_detection.py` passes.

## Non-Goals

- Do not change relative-spread math or default `threshold_percent` behavior in `detect_numeric_discrepancies()`.
- Do not add support for non-quarter period vocabularies (e.g. `FY2025`) in this issue; thesis’s `ValueError` behavior for unparseable labels stays as-is.
- No scaffolding / TODO-only changes; every task is a concrete edit verified by the gate above.

_Reproduction (current tip):_
```python
from manager_mosaic.discrepancy import FactRecord, detect_numeric_discrepancies
facts = [
    FactRecord("performance.irr", "fund-alpha", "2024Q4", 12.0, "ev-a"),
    FactRecord("performance.irr", "fund-alpha", "Q4 2024", 18.0, "ev-b"),
]
assert detect_numeric_discrepancies(facts, threshold_percent=5.0) == []  # observed: should be length 1
```

_Surfaced by Track D repo-audit 2026-09-23; verified by live probe on tip e0fe240._
