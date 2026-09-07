## Why

`pa_core/sweep.py:715` invokes simulate_agents without fee_schedule, while `pa_core/facade.py:483` supplies it for single runs. With a 10% InternalPA sleeve and 120 annual management bps, sweep annual return drag is exactly zero; the matched single-run drag is 0.001199340220. Closed issue #1904 added the working fee layer; this is its missing sweep connection.

## Scope

Apply configured fee schedules to parameter sweeps. First-party engine behavior at main 59cb12be9d4b06434d41bc1b71612167ea6d9cfc.

## Non-Goals

No unrelated refactors, synced workflow changes, new hosted service, or placeholder/scaffold-only implementation. Do not weaken the named regression to make it pass.

## Tasks

- [ ] Pass `mod_cfg.fee_schedule` at the simulate_agents call in `pa_core/sweep.py`.
- [ ] Extend `tests/test_fee_layer.py` to compare a one-point sweep and single run with deterministic inputs, nonzero fees, zero fees and an absent schedule.

## Acceptance Criteria

- [ ] The one-point sweep fee drag matches single-run economics and the absent or zero schedule remains a no-op.
- [ ] Run `pytest tests/test_fee_layer.py tests/test_sweep_config.py -q` with the added regressions and retain output.
- [ ] Deliberate-break check: Remove fee_schedule from the sweep call; the new net-versus-gross test must fail; revert.

## Implementation Notes

Severity P1. Source citations are relative to this repository. Preserve existing documented semantics outside the correction.
