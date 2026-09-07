## Why

`pa_core/sweep.py:602` resets financing generators only when standard financing is not cached. InternalPA draws at `pa_core/sweep.py:703` still advance the original internal RNG even when the other financing series are cached. An ExternalPA theta sweep changes unrelated InternalPA annual returns by -0.000139485503 with 1% InternalPA financing volatility; zero-volatility control delta is exactly zero. Existing common-random-number coverage excludes this stream; related closed #1849 added it.

## Scope

Preserve common random draws for InternalPA sweep financing. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] In `pa_core/sweep.py`, cache or reset InternalPA financing draws per combination while retaining deterministic parameter changes and avoiding accidental stream sharing.
- [ ] Extend `tests/test_sweep_common_random_numbers.py` with duplicate combinations, reordered combinations and nonzero InternalPA financing volatility under a fixed seed.

## Acceptance Criteria

- [ ] Duplicate or reordered parameter combinations retain identical InternalPA metrics when that sleeve economics is unchanged; changed financing inputs still change the result.
- [ ] Run `pytest tests/test_sweep_common_random_numbers.py tests/test_sweep_reproducibility.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Allow the original internal RNG to advance between duplicate cases; the new equality regression must fail; revert.

## Implementation Notes

Severity P2. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
