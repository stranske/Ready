## Why

`pa_core/sim/metrics.py:447` computes standard error only within the selected empirical tail; `pa_core/sim/metrics.py:463` labels the resulting interval as a confidence interval, and `pa_core/sim/metrics.py:638` exports it. The random cutoff uncertainty is not captured by the conditional tail-mean calculation. In 1000 fixed-seed normal trials with 2000 draws each, nominal 95% intervals cover the analytic lower-5% tail mean -2.0627128075074275 only 81.0% of the time. A matched normal-mean interval covers 95.9%. Closed #1917 added this feature; the requested correction concerns calibration, not feature absence.

## Scope

Calibrate the exported CVaR confidence intervals. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] In `pa_core/sim/metrics.py`, implement an estimator of CVaR sampling uncertainty that accounts for empirical-tail selection and independent paths, or withdraw the unsupported CI95 interpretation until such an estimator is available.
- [ ] Extend `tests/test_metrics.py` with a fixed-seed analytic-normal calibration gate, degenerate tails and dependent-month path fixtures. Document the resampling or asymptotic assumptions beside cvar_confidence_interval.

## Acceptance Criteria

- [ ] A retained CI95 method achieves coverage between 0.92 and 0.98 for the specified 1000-trial normal calibration and finite ordered bounds for adequate samples; alternatively unsupported CI95 columns are explicitly deprecated and no longer claimed as 95% intervals.
- [ ] Run `pytest tests/test_metrics.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Restore the conditional-tail-only interval and its CI95 export; the calibration or withdrawn-label regression must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
